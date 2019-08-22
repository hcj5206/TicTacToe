void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}
void loop() {
  bool RecvFlag=false;
  if(Serial.available()>0)
  {
    String ch =Serial.readStringUntil('\n');
    int a=ch.indexOf("<");
    int b=ch.indexOf(">");
    if(a!=-1&&b!=-1){
      String code=ch.substring(a+1,b);
      RecvFlag=true;
      ControlMode(code.toInt());
      Serial.print(code);
      Serial.print("ok");
    }
  }
    
}
bool ControlMode(int x){
    if (x==1) //take chess from board 1
      {
        Serial.print("take chess from board 1");
    }
    if (x==2) //take chess from board 2
      {
    }
    if (x==3) //take chess from board 3
      {
    }
    if (x==4) //take chess from board 4
      {
    }
    if (x==5) //take chess from board 5
      {
    }
  
  // Sub-commands for placing chesses
  
    if (x==7) //move chess to position 1
      {
    }
    if (x==8) //move chess to position 2
      {
    }
    if (x==9) //move chess to position 3
      {
    }
    if (x==10) //move chess to position 4
      {
    }
    if (x==11) //move chess to position 5
      {
    }
    if (x==12) //move chess to position 6
      {
    }
    if (x==13) //move chess to position 7  
      {
    }
    if (x==14) //move chess to position 8
      {
    }
    if (x==13) //move chess to position 9
      {
    }
    
}
