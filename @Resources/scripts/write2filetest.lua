function StatusChange()
    status = SKIN:GetVariable('PiholeStatus')
    ip = SKIN:GetVariable('PiholeIP')
    APIkey = SKIN:GetVariable('APIkey')
    FilePath = 'C:\\Users\\zeroi\\Documents\\Rainmeter\\Skins\\quancustom\\@Resources\\piholemodeswitch.txt'

    if status == 'enabled' then
        local File = io.open(FilePath, 'w')
        File:write("http://", ip, "/admin/api.php?disabled&auth=", APIkey)
	    File:close()
        SKIN:Bang("!Log Disabling_PiHole!")
    end

   if status == 'disabled' then
        local File = io.open(FilePath, 'w')
        File:write("http://", ip, "/admin/api.php?enabled&auth=", APIkey)
        File:close()
        SKIN:Bang("!Log Enabling_PiHole!")
    end



end


