-- finish later

if syntaxcheck then return end
  print("--Taken damage logger started--")
  igroTakenDamageLogger = true
  
  local CURRENT_HP_PTR = "[[[[WorldChrMan]+80]+1F90]+18]+D8"
  
  local function startDmgLogger(thread)
    local tmpHp = 0
    while(igroTakenDamageLogger) do
      local currentHp = readInteger(CURRENT_HP_PTR)
      if(currentHp ~= nil) then
        if(tmpHp > currentHp and tmpHp - currentHp > 10) then
          print("You lost "..tmpHp - currentHp.." HP")
          if(currentHp < 1) then
            print("Your died")
          end
        end
        tmpHp = currentHp
      end
      sleep(100)
    end
  end
  
  createNativeThread(startDmgLogger)

  