-- local file_path = "C:\\Users\\thanos\\OneDrive - MNSCU\\Desktop\\school\\dark_souls_ai_code\\FP-Machine-Learning\\Code\\player_info.txt"  -- Ben's path
-- local file_path = "C:\\Users\\Zach\\Desktop\\Souls\\FP-Machine-Learning\\Code\\player_info.txt" -- Zach's path
local file_path = "C:\\Users\\Laween\\OneDrive\\Desktop\\MSUM\\Spring_2025\\490\\Final_Project\\Dark_Souls\\FP-Machine-Learning\\Code\\data\\player_info.txt" -- Laween's path

function updateValues()
    local CURRENT_X_PTR = "[[[WorldChrMan]+40]+28]+80"
    local CURRENT_Z_PTR = "[[[WorldChrMan]+40]+28]+84"
    local CURRENT_Y_PTR = "[[[WorldChrMan]+40]+28]+88"
    local CURRENT_ANGLE_PTR = "[[[WorldChrMan]+40]+28]+74"
    local CURRENT_HEALTH_PTR = "[[[[WorldChrMan]+80]+1F90]+18]+D8"
    local CURRENT_STAMINA_PTR = "[[[[WorldChrMan]+80]+1F90]+18]+F0"
    local CURRENT_ESTUS_PTR = "[[WorldChrMan]+10]+5AC"
    -- local CURRENT_ESTUS_PTR = "[[[[WorldChrMan]+80]+1F90]+18]+E0"

    -- We don't need health, just use the damage taken logger

    local playerStamina = readInteger(CURRENT_STAMINA_PTR) or -999
    -- this if statement makes sure that stamina doesn't act weird
    if playerStamina > 10000 then
        playerStamina = 0
    end
    local playerX = readFloat(CURRENT_X_PTR) or -999.0
    local playerY = readFloat(CURRENT_Y_PTR) or -999.0
    local playerZ = readFloat(CURRENT_Z_PTR) or -999.0
    local playerAngle = readFloat(CURRENT_ANGLE_PTR) or -999.0
    local playerHealth = readInteger(CURRENT_HEALTH_PTR) or -999
    local playerEstus = readInteger(CURRENT_ESTUS_PTR) or -999


    -- Format the data
    local data = string.format("%d,%d,%d,%.2f,%.2f,%.2f,%.2f\n",  playerHealth, playerStamina, playerEstus, playerX, playerY, playerZ, playerAngle)

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

