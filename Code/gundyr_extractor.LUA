local file_path = "C:\\Users\\thanos\\OneDrive - MNSCU\\Desktop\\school\\dark_souls_ai_code\\FP-Machine-Learning\\Code\\gundyr_info.txt"  -- Change to your own path

function updateValues()
    local GUNDYR_HEALTH_PTR = "[[[[WorldChrMan]+80]+1F90]+18]+F0"
    local GUNDYR_X_PTR = "[[[WorldChrMan]+40]+28]+80"
    local GUNDYR_Z_PTR = "[[[WorldChrMan]+40]+28]+84"
    local GUNDYR_Y_PTR = "[[[WorldChrMan]+40]+28]+88"
    local GUNDYR_ANGLE_PTR = "[[[WorldChrMan]+40]+28]+74"


    local gundyrHealth = readInteger(GUNDYR_HEALTH_PTR) or 0
    local gundyrX = readFloat(GUNDYR_X_PTR) or 0.0
    local gundyrY = readFloat(GUNDYR_Y_PTR) or 0.0
    local gundyrZ = readFloat(GUNDYR_Z_PTR) or 0.0
    local gundyrAngle = readFloat(GUNDYR_ANGLE_PTR) or 0.0

    -- Format the data
    local data = string.format("%d,%.2f,%.2f,%.2f,%.2f\n", gundyrHealth, gundyrX, gundyrY, gundyrZ, gundyrAngle)

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
