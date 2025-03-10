-- copy of enable_flags.lua that refers to the one in autorun
-- enable_flags.lua


--  Load the main table 
loadTable("C:\\Users\\Laween\\OneDrive\\Desktop\\MSUM\\Spring_2025\\490\\Final_Project\\Dark_Souls\\FP-Machine-Learning\\DS3_Table_V1.CT")


-------------------------------------
-- Enables Main Script
-------------------------------------
local al = getAddressList()
local mainScript = al.getMemoryRecordByDescription("Open - The Grand Archives v3.4.0 - Dark Souls III v1.15.2")
if mainScript then
  mainScript.Active = true
  print("Main Script enabled!")
end

-- EVERYTHING IS IN PREP NOW SO NO NEED TO ENABLE THESE
--------------------------------------------------------------------------
-- -------------------------------------
-- -- Teleport to Boss
-- -------------------------------------
-- local TP = al.getMemoryRecordByDescription("TP to Boss")
-- if TP then
--   TP.Active = true
--   print("Teleported Sucessfully!")
-- end

-- -------------------------------------
-- -- Kills all mobs
-- -------------------------------------
-- local killMobs = al.getMemoryRecordByDescription("Kill All Mobs")
-- if killMobs then
--   killMobs.Active = true
--   print("All Mobs have been killed!")
-- end


-- -- -------------------------------------
-- -- -- Set LockOn Range to 100.0 (DEPRECATED)
-- -- -------------------------------------
-- -- local LOCKON_RANGE_PTR_STR = "[[DarkSoulsIII.exe+477DBE0]+2914]"
-- -- local lockonRangeAddr = getAddress(LOCKON_RANGE_PTR_STR)
-- -- if lockonRangeAddr then
-- --   writeFloat(lockonRangeAddr, 100.0)
-- --   print("LockOn Range set to 100.0")
-- -- else
-- --   print("LockOn Range pointer not resolved.")
-- -- end

-- -------------------------------------
-- -- Set LockOn Range to 100.0 
-- -------------------------------------
-- local lockOnRec = al.getMemoryRecordByDescription("IncreaseLockOn Range")
-- if lockOnRec then
--   lockOnRec.Active = true
--   print("IncreaseLockOn Range enabled!")
-- end
--------------------------------------------------------------------------

-------------------------------------
-- Prepare the setup
-------------------------------------
local Prep = al.getMemoryRecordByDescription("Prep")
if Prep then
  Prep.Active = true
  print("Prep enabled!")
end

-------------------------------------
-- Enables Player Logger 
-------------------------------------
local playerLogger = al.getMemoryRecordByDescription("Player Logger")
if playerLogger then
  playerLogger.Active = true
  print("Player Logger enabled!")
end

-------------------------------------
-- Enables Gundyr Logger 
-------------------------------------
local gundyrLogger = al.getMemoryRecordByDescription("Gundyr Logger")
if gundyrLogger then
  gundyrLogger.Active = true
  print("Gundyr Logger enabled!")
end

-------------------------------------
-- Enables GameManager Logger 
-------------------------------------
local gm = al.getMemoryRecordByDescription("Game Manager")
if gm then
  gm.Active = true
  print("Game Manager enabled!")
end

-----------------------------------
-- Resets the player's position to the specified coordinates after death
-----------------------------------
local Player_Reset = al.getMemoryRecordByDescription("Player Reset")
if Player_Reset then
  Player_Reset.Active = true
  print("Player Reset enabled!")
end

-----------------------------------
-- Resets the boss's flags after death
-----------------------------------
local Boss_Reset = al.getMemoryRecordByDescription("Boss Reset")
if Boss_Reset then
  Boss_Reset.Active = true
  print("Boss Reset enabled!")
end


print("All cheat engine flags/scripts enabled!")

