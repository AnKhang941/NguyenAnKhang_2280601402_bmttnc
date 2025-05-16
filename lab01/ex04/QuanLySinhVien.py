from SinhVien import SinhVien
class QuanLySinhVien:
    listSinhVien=[]
    def generateID(self):
        maxId=1
        if(self.soLuongSinhVien() >0):
            maxId= self.listSinhVien[0]._id
            for sv in self.listSinhVien:
                if(maxId<sv._id):
                    maxId=sv._id
            maxId =maxId+1
        return maxId
    def soLuongSinhVien(self):
        return self.listSinhVien.__len__()
    
    def nhapSinhVien(self):
        svId=self.generateID()
        name= input("Nhap ten sinh vien: ")
        sex=input("Nhap gioi tinh sinh vien: ")
        major= input("Nhap chuyen nganh cua sinh vien: ")
        diemTB=float(input("Nhap diem cua sinh vien: "))
        sv= SinhVien(svId,name,sex,major,diemTB)
        self.xepLoaiHocLuc(sv)
        self.listSinhVien.append(sv)
        
        
    def updateSinhVien(self,ID):
        if(sv!=None):
            name= input("Nhap ten sinh vien: ")
            sex=input("Nhap gioi tinh sinh vien: ")
            major= input("Nhap chuyen nganh cua sinh vien: ")
            diemTB=float(input("Nhap diem cua sinh vien: "))
            sv._name=name
            sv._sex=sex
            sv._major=major
            sv._diemTB=diemTB
            self.xepLoaiHocLuc(sv)
        else:
            print("sinh vien co ID={} khong ton tai.".format(ID))
    
            
            