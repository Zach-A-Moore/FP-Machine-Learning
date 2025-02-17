local file_path = "C:\\Users\\thanos\\OneDrive - MNSCU\\Desktop\\school\\dark_souls_ai_code\\FP-Machine-Learning\\Code\\player_info.txt"  -- Change to your own path

function updateValues()
    local health = readInteger(0x7FF473264AF8) or 0
    local stamina = readInteger(0x7FF473264B10) or 0
    local x = readFloat(0x7FF406020910) or 0.0
    local y = readFloat(0x7FF406020918) or 0.0
    local z = readFloat(0x7FF406020914) or 0.0
    local a = readFloat(0x7FF406020904) or 0.0

    -- Format the data
    local data = string.format("%d,%d,%.2f,%.2f,%.2f,%.2f\n", health, stamina, x, y, z, a)

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
