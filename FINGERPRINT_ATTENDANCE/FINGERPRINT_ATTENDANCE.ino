#include<EEPROM.h>
#include<LiquidCrystal.h>

//#include <Keypad.h>
LiquidCrystal lcd(8,9,10,11,12,13);

#include <SoftwareSerial.h>
SoftwareSerial fingerPrint(2, 3);


#include <Adafruit_Fingerprint.h>
uint8_t id;
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&fingerPrint);
 
#define enroll 14
#define del 15
#define up 16
#define down 17

#define records 25


int vote1,vote2,vote3;
byte data_count = 0, master_count = 0,data_count1 = 0, master_count1 = 0;  
int flag;

char ch;
void checkKeys();
int getFingerprintIDez();
String readvoice;

char Start_buff[70]; 

int a=0,b=0,c=0,d=0;
void setup()
{
//    delay(1000);
    pinMode(enroll, INPUT_PULLUP);
    pinMode(up, INPUT_PULLUP);
    pinMode(down, INPUT_PULLUP);
    pinMode(del, INPUT_PULLUP);

    
  
    fingerPrint.begin(9600);
   
   
    Serial.begin(9600);
    lcd.begin(16,2);  
    lcd.clear();
    lcd.print("ATTENDANCE ");
    lcd.setCursor(0,1);
    lcd.print("SYSTEM");
    delay(2000);
    lcd.clear();
    lcd.print("Finding Module");
    lcd.setCursor(0,1);
    delay(1000);
  
    if (finger.verifyPassword())
    {
//      Serial.println("Found fingerprint sensor!");
      lcd.clear();
      lcd.print("Found Module ");
      delay(1000);
    }
    else
    {
//    Serial.println("Did not find fingerprint sensor :(");
    lcd.clear();
    lcd.print("module not Found");
    lcd.setCursor(0,1);
    lcd.print("Check Connections");
    while (1);
    }

}
 
void loop()
{
 
START();
}

void START()
{
   while(1)
   {
     lcd.setCursor(0,0);
     lcd.print("Press UP/Down ");
     lcd.setCursor(0,1);
     lcd.print("to start System");
     if(digitalRead(up)==0 || digitalRead(down)==0)
     {
      while(1)
      {
        SerialEvent();    
      }
     }
     checkKeys();
     delay(1000);
   
   
   }  


}
void SerialEvent()
{

    fingerPrint.begin(9600);
    for(int i=0;i<5;i++)
    {
      lcd.clear();
      lcd.print("Place Finger");
      delay(2000);
      int result=getFingerprintIDez();
      if(result>=0)
      Serial.println(result);
      if(result>=0&&result<=8)
      {
        if(result==1)
        {
          lcd.clear();
          lcd.print("FINGER1 MATCHED");
          Serial.println('A');
          delay(2000);
       
        }
        if(result==2)
        {
          lcd.clear();
          lcd.print("FINGER2 MATCHED");
          Serial.println('B');
          delay(2000);
         
        }
        if(result==3)
        {
          lcd.clear();
          lcd.print("FINGER3 MATCHED");
          Serial.println('C');
       
          delay(2000);
      
        }
        if(result==4)
        {
          lcd.clear();
          lcd.print("FINGER4 MATCHED");
          Serial.println('D');
    
          delay(2000);
         
        }
        if(result==5)
        {
          lcd.clear();
          lcd.print("FINGER5 MATCHED");
          Serial.println('E');
    
          delay(2000);
         
        }
        if(result==6)
        {
          lcd.clear();
          lcd.print("FINGER6 MATCHED");
          Serial.println('F');
    
          delay(2000);
         
        }
        if(result==7)
        {
          lcd.clear();
          lcd.print("FINGER7 MATCHED");
          Serial.println('G');
    
          delay(2000);
         
        }
        if(result==8)
        {
          lcd.clear();
          lcd.print("FINGER8 MATCHED");
          Serial.println('H');
    
          delay(2000);
         
        }
       
       }
     
      
     }

} 



void checkKeys()
{
   if(digitalRead(enroll) == 0)
   {
    lcd.clear();
    lcd.print("Please Wait");
    delay(1000);
    while(digitalRead(enroll) == 0);
    Enroll();
   }
 
   else if(digitalRead(del) == 0)
   {
    lcd.clear();
    lcd.print("Please Wait");
    delay(1000);
    delet();
   }  
}

void Enroll()
{
   int count=0;
   lcd.clear();
   lcd.print("Enter Finger ID:");
   
   while(1)
   {
    lcd.setCursor(0,1);
     lcd.print(count);
     if(digitalRead(up) == 0)
     {
       count++;
       if(count>25)
       count=0;
       delay(500);
     }
 
     else if(digitalRead(down) == 0)
     {
       count--;
       if(count<0)
       count=25;
       delay(500);
     }
     else if(digitalRead(del) == 0)
     {
          id=count;
          getFingerprintEnroll();
          for(int i=0;i<records;i++)
          {
            if(EEPROM.read(i+10) == 0xff)
            {
              EEPROM.write(i+10, id);
              break;
            }
          }
          return;
     }
 
       else if(digitalRead(enroll) == 0)
     {        
          return;
     }
 }
}
 
void delet()
{
   int count=0;
   lcd.clear();
   lcd.print("Enter Finger ID");
   
   while(1)
   {
    lcd.setCursor(0,1);
     lcd.print(count);
     if(digitalRead(up) == 0)
     {
       count++;
       if(count>25)
       count=0;
       delay(500);
     }
 
     else if(digitalRead(down) == 0)
     {
       count--;
       if(count<0)
       count=25;
       delay(500);
     }
     else if(digitalRead(del) == 0)
     {
          id=count;
          deleteFingerprint(id);
          for(int i=0;i<records;i++)
          {
            if(EEPROM.read(i+10) == id)
            {
              EEPROM.write(i+10, 0xff);
              break;
            }
          }
          return;
     }
       else if(digitalRead(enroll) == 0)
     {        
          return;
     }
 }
}
 
uint8_t getFingerprintEnroll()
{
  int p = -1;
  lcd.clear();
  lcd.print("finger ID:");
  lcd.print(id);
  lcd.setCursor(0,1);
  lcd.print("Place Finger");
  delay(2000);
  while (p != FINGERPRINT_OK)
  {
    p = finger.getImage();
    switch (p)
    {
    case FINGERPRINT_OK:
      //Serial.println("Image taken");
      lcd.clear();
      lcd.print("Image taken");
      break;
    case FINGERPRINT_NOFINGER:
      //Serial.println("No Finger");
      lcd.clear();
      lcd.print("No Finger");
      break;
    case FINGERPRINT_PACKETRECIEVEERR:
      //Serial.println("Communication error");
      lcd.clear();
      lcd.print("Comm Error");
      break;
    case FINGERPRINT_IMAGEFAIL:
      //Serial.println("Imaging error");
      lcd.clear();
      lcd.print("Imaging Error");
      break;
    default:
      //Serial.println("Unknown error");
       lcd.clear();
      lcd.print("Unknown Error");
      break;
    }
  }
 
  // OK success!
 
  p = finger.image2Tz(1);
  switch (p) {
    case FINGERPRINT_OK:
      //Serial.println("Image converted");
      lcd.clear();
      lcd.print("Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      //Serial.println("Image too messy");
       lcd.clear();
       lcd.print("Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      //Serial.println("Communication error");
            lcd.clear();
      lcd.print("Comm Error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      //Serial.println("Could not find fingerprint features");
            lcd.clear();
      lcd.print("Feature Not Found");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      //Serial.println("Could not find fingerprint features");
                  lcd.clear();
      lcd.print("Feature Not Found");
      return p;
    default:
      //Serial.println("Unknown error");
                  lcd.clear();
      lcd.print("Unknown Error");
      return p;
  }
 
  //Serial.println("Remove finger");
  lcd.clear();
  lcd.print("Remove Finger");
  delay(2000);
  p = 0;
  while (p != FINGERPRINT_NOFINGER) {
    p = finger.getImage();
  }
  //Serial.print("ID "); //Serial.println(id);
  p = -1;
  //Serial.println("Place same finger again");
   lcd.clear();
      lcd.print("Place Finger");
      lcd.setCursor(0,1);
      lcd.print("   Again");
  while (p != FINGERPRINT_OK) {
    p = finger.getImage();
    switch (p) {
    case FINGERPRINT_OK:
      //Serial.println("Image taken");
      break;
    case FINGERPRINT_NOFINGER:
      //Serial.print(".");
      break;
    case FINGERPRINT_PACKETRECIEVEERR:
      //Serial.println("Communication error");
      break;
    case FINGERPRINT_IMAGEFAIL:
      //Serial.println("Imaging error");
      break;
    default:
      //Serial.println("Unknown error");
      return;
    }
  }
 
  // OK success!
 
  p = finger.image2Tz(2);
  switch (p) {
    case FINGERPRINT_OK:
      //Serial.println("Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      //Serial.println("Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      //Serial.println("Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      //Serial.println("Could not find fingerprint features");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      //Serial.println("Could not find fingerprint features");
      return p;
    default:
      //Serial.println("Unknown error");
      return p;
  }
 
  // OK converted!
  //Serial.print("Creating model for #");  //Serial.println(id);
 
  p = finger.createModel();
  if (p == FINGERPRINT_OK) {
    //Serial.println("Prints matched!");
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    //Serial.println("Communication error");
    return p;
  } else if (p == FINGERPRINT_ENROLLMISMATCH) {
    //Serial.println("Fingerprints did not match");
    return p;
  } else {
    //Serial.println("Unknown error");
    return p;
  }  
 
  //Serial.print("ID "); //Serial.println(id);
  p = finger.storeModel(id);
  if (p == FINGERPRINT_OK) {
    //Serial.println("Stored!");
    lcd.clear();
    lcd.print("Stored!");
    delay(2000);
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    //Serial.println("Communication error");
    return p;
  } else if (p == FINGERPRINT_BADLOCATION) {
    //Serial.println("Could not store in that location");
    return p;
  } else if (p == FINGERPRINT_FLASHERR) {
    //Serial.println("Error writing to flash");
    return p;
  }
  else {
    //Serial.println("Unknown error");
    return p;
  }  
}
 
int getFingerprintIDez()
{
  uint8_t p = finger.getImage();
 
  if (p != FINGERPRINT_OK)  
  return -1;
 
  p = finger.image2Tz();
  if (p != FINGERPRINT_OK)  
  return -1;
 
  p = finger.fingerFastSearch();
  if (p != FINGERPRINT_OK)
  {
   lcd.clear();
   lcd.print("Finger Not Found");
   lcd.setCursor(0,1);
   lcd.print("Try Later");
   
   
  
  return 9;
  }
  // found a match!
//  Serial.print("Found ID #");
 // Serial.print(finger.fingerID);
 while(1)
 {
    switch(finger.fingerID)
       {
      case 1:lcd.clear();
             lcd.print("NAME:NAVEN");
             lcd.setCursor(0,1);
             lcd.print("AGE:20");
//             digitalWrite(door,HIGH);
//              delay(50);
//              digitalWrite(door,LOW);  
             return finger.fingerID;
             break;

       case 2:lcd.clear();
             lcd.print("NAME:BBBB");
             lcd.setCursor(0,1);
             lcd.print("AGE:21");
//               digitalWrite(door,HIGH);
//              delay(50);
//                digitalWrite(door,LOW);   
             return finger.fingerID;
             break;

      case 3:lcd.clear();
             lcd.print("NAME:CCCC");
             lcd.setCursor(0,1);
             lcd.print("AGE:22");
//              digitalWrite(door,HIGH);
//             delay(50);  
//              digitalWrite(door,LOW);  
             return finger.fingerID;
             break;

      case 4:lcd.clear();
             lcd.print("NAME:DDDDD");
             lcd.setCursor(0,1);
             lcd.print("AGE:23");
//              digitalWrite(door,HIGH);
//             delay(50);
//              digitalWrite(door,LOW);    
             return finger.fingerID;
             break;

       case 5:lcd.clear();
             lcd.print("CCCCCC");
             lcd.setCursor(0,1);
             lcd.print("AGE:24");
//              digitalWrite(door,HIGH);
//             delay(50); 
//              digitalWrite(door,LOW);   
             return finger.fingerID;
             break;

       case 6:lcd.clear();
             lcd.print("DDDDDD");
             lcd.setCursor(0,1);
             lcd.print("AGE:25");
//              digitalWrite(door,HIGH);
//             delay(50);
//              digitalWrite(door,LOW);  
             return finger.fingerID;
             break;

       case 7:lcd.clear();
             lcd.print("EEEEE");
             lcd.setCursor(0,1);
             lcd.print("AGE:26");
//             digitalWrite(door,HIGH);
//             delay(50);
//              digitalWrite(door,LOW);  
             return finger.fingerID;
             break;
       
  }  
 }
  return finger.fingerID;
}
 
uint8_t deleteFingerprint(uint8_t id)
{
  uint8_t p = -1;  
  lcd.clear();
  lcd.print("Please wait");
  p = finger.deleteModel(id);
  if (p == FINGERPRINT_OK)
  {
    //Serial.println("Deleted!");
    lcd.clear();
    lcd.print("Finger Deleted");
    lcd.setCursor(0,1);
    lcd.print("Successfully");
    delay(1000);
  }
 
  else
  {
    //Serial.print("Something Wrong");
    lcd.clear();
    lcd.print("Something Wrong");
    lcd.setCursor(0,1);
    lcd.print("Try Again Later");
    delay(2000);
    return p;
  }  
}
