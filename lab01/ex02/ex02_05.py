so_gio_lam =float(input("Nhap so gio lam moi tuan: "))
luong_gio = float(input("Nhap thu lao moi luong gio tieu chuan: "))

gio_tieu_chuan = 44
gio_vuot_chuan = max(0,so_gio_lam - gio_tieu_chuan)
thuc_linh = gio_tieu_chuan *luong_gio + gio_vuot_chuan *luong_gio*1.5
print("so tien thuc linh: ", thuc_linh)
