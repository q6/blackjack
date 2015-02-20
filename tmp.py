CSI="\x1B["
reset=CSI+"m"
print(CSI+"31;40m" + "Colored Text" + CSI + "0m")