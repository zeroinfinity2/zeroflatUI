[Variables]
;Pihole API Token (Get API Token in PiHole GUI, required for top blocked stats)
APIkey=8f13eb8fa9e41511a63bc2f748d3840f39f9bc25531cc1272fe1e15f82ee23f8

;PiHole IP Address (see documentation to make a static address)
PiholeIP=192.168.1.3

;Pihole API Links (Don't change unless PiHole changes their API)
statusURL=http://#PiholeIP#/admin/api.php?status&auth=#APIkey#
rawSummaryURL=http://#PiholeIP#/admin/api.php?summaryRaw
topURL=http://#PiholeIP#/admin/api.php?topItems=5&auth=#APIkey#
recentURL=http://#PiholeIP#/admin/api.php?recentBlocked&auth=#APIkey#
disableURL=http://#PiholeIP#/admin/api.php?disable&auth=#APIkey#
enableURL=http://#PiholeIP#/admin/api.php?enable&auth=#APIkey#