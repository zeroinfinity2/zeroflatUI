[Variables]
;Pihole API Token (Get API Token in PiHole GUI, required for top blocked stats)
APIkey=

;PiHole IP Address (see documentation to make a static address)
PiholeIP=

;Pihole API Links (Don't change unless PiHole changes their API)
statusURL=http://#PiholeIP#/admin/api.php?status&auth=#APIkey#
rawSummaryURL=http://#PiholeIP#/admin/api.php?summaryRaw
topURL=http://#PiholeIP#/admin/api.php?topItems=5&auth=#APIkey#
recentURL=http://#PiholeIP#/admin/api.php?recentBlocked&auth=#APIkey#
disableURL=http://#PiholeIP#/admin/api.php?disable&auth=#APIkey#
enableURL=http://#PiholeIP#/admin/api.php?enable&auth=#APIkey#