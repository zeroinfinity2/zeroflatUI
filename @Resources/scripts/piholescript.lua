function setAngles()
    -- Handlers
    getTopHandle1 = SKIN:GetMeasure('MeasureTopPercent1')
    getTopHandle2 = SKIN:GetMeasure('MeasureTopPercent2')
    getTopHandle3 = SKIN:GetMeasure('MeasureTopPercent3')
    getTopHandle4 = SKIN:GetMeasure('MeasureTopPercent4')

    --Get Values from Handles
    perc1 = getTopHandle1:GetValue()
    perc2 = getTopHandle2:GetValue()
    perc3 = getTopHandle3:GetValue()
    perc4 = getTopHandle4:GetValue()

    --Determine STARTING angles (except for angle1, which will start at 0)
    angle2 = math.floor((perc1 / 100) * 360)
    angle3 = math.floor((perc2 / 100) * 360) + angle2
    angle4 = math.floor((perc3 / 100) * 360) + angle3
    angle5 = math.floor((perc4 / 100) * 360) + angle4

    --Set the Angles
    SKIN:Bang("!Log Setting_Angle_Variables")
    SKIN:Bang('!SetVariable', 'startAngle2', angle2)
    SKIN:Bang('!SetVariable', 'startAngle3', angle3)
    SKIN:Bang('!SetVariable', 'startAngle4', angle4)
    SKIN:Bang('!SetVariable', 'startAngle5', angle5)  

end

function StatusChange(status)
    if status == 'enabled' then
        SKIN:Bang("!Log Disabling_PiHole!")
        SKIN:Bang('!ActivateConfig', 'quancustom\\piholestats', 'piholeOFF.ini')
    
    elseif status == 'disabled' then
        SKIN:Bang("!Log Enabling_PiHole!")
        SKIN:Bang('!ActivateConfig', 'quancustom\\piholestats', 'piholeON.ini')
    end
end