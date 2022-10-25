function Update()
    hourOfDay = tonumber(os.date('%H'))

    if hourOfDay >= 18 or hourOfDay <= 4 then
        SKIN:Bang('!SetVariable', 'NightDay', 'night')
    else
        SKIN:Bang('!SetVariable', 'NightDay', 'day')
    end
end