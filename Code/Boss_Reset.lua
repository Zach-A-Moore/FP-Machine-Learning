[ENABLE]
{$lua}

-- 1) Define pointer strings
local PLAYER_HEALTH_PTR_STR = "[[[[WorldChrMan]+80]+1F90]+18]+D8"
local BOSS_HEALTH_PTR_STR   = "[[[[[[[DarkSoulsIII.exe+049648F8]+98]+200]+28]+168]+10]+F0]+F28"  -- uses target_ptr from "Target Entity Info"
local BOSS_FLAGS_PTR        = "[[SprjEventFlagMan]+0]+5A67"

-- 2) killPlayer function (must come before reviveBoss so it's not nil)
local function killPlayer()
  local curHPAddr = getAddress(PLAYER_HEALTH_PTR_STR)
  if not curHPAddr or curHPAddr == 0 then
    print("[BossReset] ERROR: Could not find player HP pointer.")
    return
  end
  -- Wait 5 seconds, then set HP to 0
  sleep(5000)
  writeInteger(curHPAddr, 0)
  print("[BossReset] Player killed (HP set to 0).")
end

-- 3) reviveBoss function
local function reviveBoss()
  local BOSS_FLAGS_ADDR = getAddress(BOSS_FLAGS_PTR)
  -- Read a single byte (3rd param omitted => integer instead of table)
  local currentValue = readBytes(BOSS_FLAGS_ADDR, 1)
  if not currentValue then
    print("[BossReset] ERROR: Could not read boss flags.")
    return
  end

local al = getAddressList()
  local Rez = al.getMemoryRecordByDescription("Resurrect all Bosses")
if Rez then
  Rez.Active = true
  print("All Bosses Resurrected!")
end
  -- Clear bit 7 (Defeated) and set bits 6 & 5 (Encountered + Pulled Sword Out)
  currentValue = currentValue & 0x7F  -- Clear bit 7
  currentValue = currentValue | 0x60  -- Set bits 6 and 5

  writeBytes(BOSS_FLAGS_ADDR, currentValue)
  print(string.format("[BossReset] Boss revived. New flags = 0x%X", currentValue))

  -- Double-check the new value. If it matches, kill the player
--  local newVal = readBytes(BOSS_FLAGS_ADDR, 1)
--  if newVal == currentValue then
--    killPlayer()
--  else
--    print("[BossReset] Boss flags not updated. Not killing player.")
--  end
end

-- 4) Track death times to add a delay
local bossDeathTime = nil

-- 5) Main loop that checks health and triggers resets
local function checkAndReset()
  local bossHPAddr = getAddress(BOSS_HEALTH_PTR_STR)
  if not bossHPAddr or bossHPAddr == 0 then
    print("[BossReset] Boss pointer invalid. Possibly wrong pointer.")
    return
  end

  -- Read health
  local bHP = readInteger(bossHPAddr) or -1
  print(string.format("[BossReset] Checking BossHP=%d", bHP))

  -- Boss death => wait 5s => revive
  if bHP == 0 then
    if not bossDeathTime then
      bossDeathTime = os.time()
      print("[BossReset] Boss death detected. Waiting 5s before revive.")
    elseif os.time() - bossDeathTime >= 5 then
      reviveBoss()
      killPlayer()
      bossDeathTime = nil
    end
  end
end

-- 6) Create and enable a timer that checks every 1000ms
bossResetTimer = createTimer(nil, false)
bossResetTimer.Interval = 1000
bossResetTimer.OnTimer = checkAndReset
bossResetTimer.setEnabled(true)
print("[BossReset] Timer enabled. Boss reset script active.")

{$asm}

[DISABLE]
{$lua}
-- Cleanup
if bossResetTimer then
  bossResetTimer.destroy()
  bossResetTimer = nil
end
{$asm}
