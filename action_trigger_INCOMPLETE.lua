[ENABLE]
{$lua}
local file_path = "C:\\Users\\Laween\\OneDrive\\Desktop\\MSUM\\Spring_2025\\490\\Final_Project\\Dark_Souls\\FP-Machine-Learning\\Code\\data\\action_trigger.txt"
local VK_W = 0x57  -- W key for movement
local VK_LBUTTON = 0x01  -- Left mouse button
local VK_SPACE = 0x20  -- Space for dodge
local VK_R = 0x52  -- R for heal

function pressKey(vk)
  executeCodeLocal(getProcAddressByExport("user32.dll", "keybd_event"), vk, 0, 0, 0) -- keydown
  sleep(50)
  executeCodeLocal(getProcAddressByExport("user32.dll", "keybd_event"), vk, 0, 2, 0) -- keyup
end

function execute_action()
  local file = io.open(file_path, "r")
  if file then
    local line = file:read("*line")
    file:close()
    if line then
      local command, movement = line:match("(%d+),([-]?%d+%.?%d*)")
      command = tonumber(command)
      movement = tonumber(movement)
      if command == 0 then pressKey(VK_LBUTTON) end  -- Attack
      if command == 1 then pressKey(VK_SPACE) end   -- Dodge
      if command == 2 then pressKey(VK_R) end       -- Heal
      if movement then
        local duration = math.abs(movement) * 0.2  -- Scale movement to time
        if movement > 0 then pressKey(VK_W) end    -- Forward
        if movement < 0 then pressKey(VK_S) end    -- Backward (add S key logic in control_ds3_ml.py)
      end
    end
  end
end

actionTimer = createTimer(nil, false)
actionTimer.Interval = 100
actionTimer.OnTimer = execute_action
actionTimer.setEnabled(true)
{$asm}

[DISABLE]
{$lua}
if actionTimer then
  actionTimer.destroy()
  actionTimer = nil
end
{$asm}

