local file_path = "C:\\Users\\Laween\\Downloads\\game_data.txt"  -- Change to your own path

function updateValues()
    local health = readInteger(0x7FF473264AF8) or 0
    local stamina = readInteger(0x7FF473264B10) or 0
    local x = readFloat(0x7FF473266110) or 0.0
    local y = readFloat(0x7FF473266118) or 0.0
    local z = readFloat(0x7FF473266114) or 0.0

    -- Format the data
    local data = string.format("%d,%d,%.2f,%.2f,%.2f\n", health, stamina, x, y, z)

    -- Open file for writing
    local file = io.open(file_path, "w")
    if file then
        file:write(data)
        file:close()
    end
end

if myTimer then
    myTimer.destroy()
end

myTimer = createTimer(nil, false)
myTimer.Interval = 100  -- in ms
myTimer.OnTimer = updateValues
myTimer.setEnabled(true)

myTimer.destroy()
