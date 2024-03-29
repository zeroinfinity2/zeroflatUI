function colors(colorText, alphaPercent)
	
	colorText = string.lower(colorText)
	colorValues = {
		['white'] = '255,255,255,', 
		['cyan'] = '50,234,255,',
		['black'] = '0,0,0,',
		['gray'] = '162,162,162,',
		['orange'] = '235,160,94,',
		['pink'] = '255,76,125,',
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