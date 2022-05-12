import xml.etree.ElementTree as ET
import xml

def main(file_name):
    #xmlファイル読み込み
    tree = ET.parse(file_name+'.xml')
    root = tree.getroot()

    #ボックスの座標が書かれている
    for i in root.iter('bndbox'):
        return i.find("xmin").text,i.find("ymin").text,i.find("xmax").text,i.find("ymax").text
        #i.find("xmin").text= str(float(i.find("xmin").text)*100)
    #tree.write('A.xml', encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    print(main("mausu"))
    