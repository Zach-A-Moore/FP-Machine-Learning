[ENABLE]
{$lua}
local bossBattleAddr = getAddress("[[GameDataMan]+C0]")
local playerHPAddr   = getAddress("[[[[WorldChrMan]+80]+1F90]+18]+D8")

local inBossFight = readByte(bossBattleAddr) or 0
local playerHP    = readInteger(playerHPAddr) or 0


if inBossFight == 0 and playerHP > 0 then

local al = getAddressList()
local lockOnRec = al.getMemoryRecordByDescription("Increase LockOn Range")
if lockOnRec then
  lockOnRec.Value = "100"
  lockOnRec.Frozen = true
  print("[IncreaseLockOnRange] Successfully froze lock-on range at 100.")
else
  print("[IncreaseLockOnRange] ERROR: Memory record 'Increase LockOn Range' not found!")
end
end
{$asm}

[DISABLE]
{$lua}
local al = getAddressList()
local lockOnRec = al.getMemoryRecordByDescription("Increase LockOn Range")
if lockOnRec then
  lockOnRec.Frozen = false
  lockOnRec.Value = "0"
  print("[IncreaseLockOnRange] Lock-on range unfrozen and set to 0.")
end
{$asm}
