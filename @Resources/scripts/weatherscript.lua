function Update()
    hourOfDay = tonumber(os.date('%H'))

    if hourOfDay >= 18 or hourOfDay <= 6 then
        SKIN:Bang('!SetVariable', 'NightDay', 'night')
    else
        SKIN:Bang('!SetVariable', 'NightDay', 'day')
    end

    SKIN:Bang('!SetVariable', 'HourSlot', (hourOfDay))

end

function NextDay(daysToSkip)
    today = tonumber(os.date('%w'))
    days = {'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'}
    return days[((today + daysToSkip) % 7) + 1]
end