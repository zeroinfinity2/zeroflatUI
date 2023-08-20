function colors(colorText, alphaPercent)
	
	colorText = string.lower(colorText)
	colorValues = {
		['white'] = '255,255,255,', 
		['blue-white'] = '183,200,198,',
		['sky-blue'] = '213, 235, 232, ', 
		['cyan'] = '53,196,233,',
		['blue-green'] = '86,189,174,',
		['black'] = '0,0,0,',
		['gray'] = '162,162,162,',
		['orange'] = '201,103,51,',
		['pink'] = '255,76,125,',
		['light-pink'] = '255,241,241,',
		['blue'] = '97,195,255,',
		['yellow'] = '255,232,64,',
		['purple'] = '150,99,235,'}
		
	if alphaPercent <= 100 and alphaPercent >= 0 then
		alpha = math.floor((alphaPercent / 100) * 255)
	else
		alpha = 0
	end

	colorSelect = colorValues[colorText] .. tostring(alpha)
	return colorSelect

end