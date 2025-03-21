[ENABLE]
{$lua}
-- Destroy any previous timer if it exists
if myTimer then
    myTimer.destroy()
end
-- local file_path = "C:\\Users\\thanos\\OneDrive - MNSCU\\Desktop\\school\\dark_souls_ai_code\\FP-Machine-Learning\\Code\\gundyr_info.txt"  -- Ben's path
-- local lab_file_path = "C:\\Users\\Zach\\Desktop\\Souls\\FP-Machine-Learning\\Code\\player_info.txt" -- Zach's path
local file_path = "C:\\Users\\Laween\\OneDrive\\Desktop\\MSUM\\Spring_2025\\490\\Final_Project\\Dark_Souls\\FP-Machine-Learning\\Code\\data\\gundyr_info.txt" -- Laween's path

function updateValues()
    -- if player is locked onto Gundyr, these are his pointers
    local GUNDYR_HEALTH_PTR = "[[[target_ptr]+1F90]+18]+D8"
    local GUNDYR_X_PTR = "[[[[[target_ptr]+1F90]+68]+A8]+40]+70"
    local GUNDYR_Z_PTR = "[[[[[target_ptr]+1F90]+68]+A8]+40]+74"
    local GUNDYR_Y_PTR = "[[[[[target_ptr]+1F90]+68]+A8]+40]+7C"
    local GUNDYR_ANGLE_PTR = "[[[[[target_ptr]+1F90]+68]+A8]+40]+70"
    local CURRENT_ANIM_NAME_PTR = "[[[target_ptr]+1F90]+28]+898"


    local gundyrHealth = readInteger(GUNDYR_HEALTH_PTR) or -999
    local gundyrX = readFloat(GUNDYR_X_PTR) or -999.0
    local gundyrY = readFloat(GUNDYR_Y_PTR) or -999.0
    local gundyrZ = readFloat(GUNDYR_Z_PTR) or -999.0
    local gundyrAngle = readFloat(GUNDYR_ANGLE_PTR) or -999.0
    local gundyrAnim = readString(CURRENT_ANIM_NAME_PTR) or nil

    -- Format the data
    local data = string.format("%d,%.2f,%.2f,%.2f,%.2f,%s\n", gundyrHealth, gundyrX, gundyrY, gundyrZ, gundyrAngle, gundyrAnim)

    -- Open file for writing
    local file = io.open(file_path, "w")
    if file then
        file:write(data)
        file:close()
    end
end


myTimer = createTimer(nil, false)
myTimer.Interval = 100  -- in ms
myTimer.OnTimer = updateValues
myTimer.setEnabled(true)
{$asm}


[DISABLE]
{$lua}
-- Destroy the timer when disabling the script
if myTimer then
    myTimer.destroy()
    myTimer = nil
end
{$asm}

