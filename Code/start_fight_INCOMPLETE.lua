[ENABLE]
{$lua}

------------------------------------------------------------
-- 0) Helper functions (case-insensitive module search)
------------------------------------------------------------
function getModuleBaseByName(modname)
  local mods = enumModules()
  if not mods then
    return nil
  end

  local modLower = modname:lower()
  for i, m in ipairs(mods) do
    if m.Name:lower() == modLower then
      return m.Address, m.Name  -- Return both the address and exact name
    end
  end
  return nil
end

function getProcAddressByExport(modname, exportname)
  local base, realName = getModuleBaseByName(modname)
  if not base or not realName then
    return nil
  end

  local exports = enumExports(realName)
  if not exports then
    return nil
  end

  for i, e in ipairs(exports) do
    if e.Name == exportname then
      return e.Address
    end
  end
  return nil
end

------------------------------------------------------------
-- 1) Find USER32.dll and keybd_event (case-insensitive)
------------------------------------------------------------
local keybd_event_addr = getProcAddressByExport("user32.dll", "keybd_event")
if not keybd_event_addr then
  print("ERROR: Could not find 'keybd_event' export in user32.dll!")
  getScript().Active = false
  return
end

------------------------------------------------------------
-- 2) Define pressKey function (uses keybd_event_addr)
------------------------------------------------------------
function pressKey(vk)
  -- KEYEVENTF_KEYDOWN = 0
  -- KEYEVENTF_KEYUP   = 2
  executeCodeLocal(keybd_event_addr, vk, 0, 0, 0) -- keydown
  sleep(50)
  executeCodeLocal(keybd_event_addr, vk, 0, 2, 0) -- keyup
end

-- Virtual-key codes for E and Q
local VK_E = 0x45
local VK_Q = 0x51

------------------------------------------------------------
-- 3) Define pointer strings for player coords & angle
------------------------------------------------------------
local CURRENT_X_PTR = "[[[WorldChrMan]+40]+28]+80"
local CURRENT_Z_PTR = "[[[WorldChrMan]+40]+28]+84"
local CURRENT_Y_PTR = "[[[WorldChrMan]+40]+28]+88"
local CURRENT_ANGLE_PTR = "[[[WorldChrMan]+40]+28]+74"

-- Desired angle (radians) for facing the fog wall
local targetAngle = -2.778103352
-- Distance to move forward
local moveDistance = 5

------------------------------------------------------------
-- 4) Set player's angle
------------------------------------------------------------
local angleAddr = getAddressSafe(CURRENT_ANGLE_PTR)
if angleAddr then
  writeFloat(angleAddr, targetAngle)
  print("Player angle set to:", targetAngle)
else
  print("ERROR: Could not resolve angle pointer!")
  getScript().Active = false
  return
end

------------------------------------------------------------
-- 5) Move the player 5 units forward
------------------------------------------------------------
local xAddr = getAddressSafe(CURRENT_X_PTR)
local zAddr = getAddressSafe(CURRENT_Z_PTR)
if (not xAddr) or (not zAddr) then
  print("ERROR: Could not resolve X/Z pointers!")
  getScript().Active = false
  return
end

local currentX = readFloat(xAddr)
local currentZ = readFloat(zAddr)
print("Current position: X =", currentX, "Z =", currentZ)

-- Simple trig: newX = oldX + distance*cos(angle)
--              newZ = oldZ + distance*sin(angle)
local newX = currentX + moveDistance * math.cos(targetAngle)
local newZ = currentZ + moveDistance * math.sin(targetAngle)

-- Write new coords
writeFloat(xAddr, newX)
writeFloat(zAddr, newZ)
print("Moved player to X =", newX, "Z =", newZ)

------------------------------------------------------------
-- 6) Interact with fog wall: press E
------------------------------------------------------------
print("Pressing E to interact with fog wall...")
pressKey(VK_E)

------------------------------------------------------------
-- 7) Wait 1 second, then lock on with Q
------------------------------------------------------------
sleep(1000)
print("Pressing Q to lock on to boss...")
pressKey(VK_Q)

------------------------------------------------------------
-- 8) Disable script so it runs only once
------------------------------------------------------------
getScript().Active = false

{$asm}

[DISABLE]
{$lua}
-- No cleanup needed
{$asm}
