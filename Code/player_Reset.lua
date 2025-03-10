[ENABLE]
{$lua}

----------------------------------------
-- 1) Define pointer strings and variables
----------------------------------------
local PLAYER_HEALTH_PTR_STR = "[[[[WorldChrMan]+80]+1F90]+18]+D8"
local LUDEX_TARGET_STR       = "[[[WorldChrMan]+40]+28]+80"
local CURRENT_ANGLE_PTR      = "[[[WorldChrMan]+40]+28]+74"


local WAIT_SECS = 20000  -- wait 10 seconds after death

local playerDeathTime = 0  -- 0 means no death detected yet
local hasReset = false     -- flag to ensure reset is only done once per death



local function reset()
      sleep(20000)
  local al = getAddressList()
  local prep = al.getMemoryRecordByDescription("Prep")
  if prep then
    prep.Active = true
    print("Script 'Prep' enabled.")
  else
    print("Script 'Prep' not found.")
  end

  end




----------------------------------------
-- 2) Ludex script function (writing bytes)
----------------------------------------
local function writeLudexBytes()
sleep(WAIT_SECS)
hasReset = true
  writeBytes(LUDEX_TARGET_STR,
    0x93, 0xE6, 0xF8, 0x42,
    0x6D, 0xD0, 0x7F, 0xC2,
    0xC7, 0xF3, 0x0A, 0x44
  )
  print("[P_Reset] Ludex bytes written manually.")

-- Set desired angle
local targetAngle = -2.778103352
local angleAddr = getAddressSafe(CURRENT_ANGLE_PTR)
if angleAddr then
  writeFloat(angleAddr, targetAngle)
  print("Player angle set to:", targetAngle)
else
  print("ERROR: Could not resolve angle pointer!")
  getScript().Active = false
  return
end

end

----------------------------------------
-- 3) Timer callback function (re-resolves pointer each time)
----------------------------------------
local function checkAndReset()
  -- Re-resolve the player HP pointer each time to ensure we get an updated value.
  local curHPAddr = getAddress(PLAYER_HEALTH_PTR_STR)
  local hp = (curHPAddr and readInteger(curHPAddr)) or -1
  print(string.format("[P_Reset] Checking PlayerHP=%d", hp))

  if hp <= 0 then
    if playerDeathTime == 0 then
      playerDeathTime = os.time()
      print("[P_Reset] Player death detected. Waiting " .. WAIT_SECS .. " seconds before reset.")
      reset()
    end
    if not hasReset and hp > 0 then
      print("[P_Reset] Setting hasReset to true.")
      hasReset = true
    end
  else
    if playerDeathTime ~= 0 then
      print("[P_Reset] Player revived. Resetting death state.")
      playerDeathTime = 0
      hasReset = false
    end
  end
end

----------------------------------------
-- 4) Create and enable the timer
----------------------------------------
playerResetTimer = createTimer(nil, false)
playerResetTimer.Interval = 1000  -- check every 100ms
playerResetTimer.OnTimer = checkAndReset
playerResetTimer.setEnabled(true)
print("[P_Reset] Timer enabled. Player reset script active.")

{$asm}

[DISABLE]
{$lua}
if playerResetTimer then
  playerResetTimer.destroy()
  playerResetTimer = nil
end
{$asm}
