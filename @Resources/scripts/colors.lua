function colors(colortext, alphapercent)
	if colortext == 'white' then 
		color = '255,255,255,'
	elseif colortext == 'cyan' then
		color = '50,234,255,'
	elseif colortext == 'black' then
		color = '0,0,0,'
	elseif colortext == 'gray' then
		color = '162,162,162,'
	elseif colortext == 'orange' then
		color = '235,160,94,'
	elseif colortext == 'pink' then
		color = '255,76,125,'
	elseif colortext == 'blue' then
		color = '97,195,255,'
	elseif colortext == 'yellow' then
		color = '255,232,64,'
	elseif colortext == 'purple' then
		color = '150,99,235,'
	end	
		
	if alphapercent <= 100 and alphapercent >= 0 then
		alpha = math.floor((alphapercent / 100) * 255)
	else
		alpha = 0
	end

	colorselect = color .. tostring(alpha)
	return colorselect

end