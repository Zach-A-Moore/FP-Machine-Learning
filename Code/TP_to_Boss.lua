[ENABLE]
{$lua}
-- Define pointer strings
local PLAYER_HEALTH_PTR_STR = "[[[[WorldChrMan]+80]+1F90]+18]+D8"
local LUDEX_TARGET_STR       = "[[[WorldChrMan]+40]+28]+80"
local CURRENT_ANGLE_PTR      = "[[[WorldChrMan]+40]+28]+74"

-- Write the desired bytes (this action is performed only once)
writeBytes(LUDEX_TARGET_STR,
  0x93, 0xE6, 0xF8, 0x42,
  0x6D, 0xD0, 0x7F, 0xC2,
  0xC7, 0xF3, 0x0A, 0x44
)
print("[TP] Teleported Successfully!")


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

-- Freeze angle for 3 seconds to override external tool influences
--local freezeDuration = 3.0  -- seconds
--local startTime = os.clock()
--while (os.clock() - startTime) < freezeDuration do
--  writeFloat(angleAddr, targetAngle)
--  sleep(100)
--end
--print("Player angle frozen for", freezeDuration, "seconds.")


-- Automatically disable this script so it runs only once
getScript().Active = false
{$asm}

[DISABLE]
{$lua}

{$asm}
