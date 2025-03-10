-- initial position pointer
local INITPOS_PTR = getAddress("[GameMan]+A40")

-- array of good initial position
-- TODO: make sure the desired position is not too close tothe fog wall
local desiredPosition = {0xA8, 0x18, 0xFB, 0x42, 0xD6, 0x19, 0x80, 0xC2, 0x1E, 0xD0, 0x0B, 0x44}

-- get the current initial position
local currentPosition = readBytes(INITPOS_PTR, #desiredPosition, true)

-- check if they match
local match = true
for i = 1, #desiredPosition do
    if currentPosition[i] ~= desiredPosition[i] then
        match = false
        break
    end
end

-- update if there's no match
if not match then
    writeBytes(INITPOS_PTR, table.unpack(desiredPosition))
    print("Memory updated to desired byte array.")
else
    print("Memory already matches desired value.")
end