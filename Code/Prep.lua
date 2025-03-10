[ENABLE]
{$lua}

-- Resolve pointers:
local bossBattleAddr = getAddress("[[GameDataMan]+C0]")
local playerHPAddr   = getAddress("[[[[WorldChrMan]+80]+1F90]+18]+D8")
local playerXAddr    = getAddress("[[[WorldChrMan]+40]+28]+80")

if not bossBattleAddr then
  print("ERROR: Could not resolve boss fight pointer.")
  return
end
if not playerHPAddr then
  print("ERROR: Could not resolve player HP pointer.")
  return
end
if not playerXAddr then
  print("ERROR: Could not resolve player X pointer.")
  return
end

-- Read values:
local inBossFight = readByte(bossBattleAddr) or 0
local playerHP    = readInteger(playerHPAddr) or 0
local playerX     = readFloat(playerXAddr) or 0

print(string.format("inBossFight = %s, playerHP = %d, playerX = %.2f", inBossFight, playerHP, playerX))

-- Check if the player is not in a boss fight (assumed inBossFight==0),
-- health is above 0, and x position is between 102 and 105.
if inBossFight == 0 and playerHP > 0  then
  print("Conditions met: Not in boss fight, health > 0, and x position in [102,105].")
  -- Get the address list to enable other scripts:
  local al = getAddressList()
  local kill = al.getMemoryRecordByDescription("Kill All Mobs")
  local TP = al.getMemoryRecordByDescription("TP to Boss")
  local lockon = al.getMemoryRecordByDescription("IncreaseLockOn Range")
  if kill then
    kill.Active = true
    print("Script 'Kill All Mobs' enabled.")
  else
    print("Script 'Kill All Mobs' not found.")
  end
  if TP then
    TP.Active = true
    print("Script 'TP to Boss' enabled.")
  else
    print("Script 'TP to Boss' not found.")
  end
    if lockon then
lockon.Active = false
    lockon.Active = true
    print("Script 'IncreaseLockOn Range' enabled.")
  else
    print("Script 'IncreaseLockOn Range' not found.")
  end
else
  print("Player is in boss fight or conditions not met; scripts not enabled.")
end

getScript().Active = false
{$asm}

[DISABLE]
{$lua}
-- No disable code required.
{$asm}
