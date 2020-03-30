int nMuestras=100;
void setup()
{
  Serial.begin(9600);
}

void loop()
{
  float instVolatage, Vpp, Irms;
  float minVoltage=5.0, maxVoltage=0.0;
  for(int i=0; i<nMuestras;i++)
  {
    instVolatage = 5.0/1023*analogRead(A0);
    if(instVolatage<= minVoltage)minVoltage=instVolatage;
    if(instVolatage>= maxVoltage)maxVoltage=instVolatage;
  }
  Vpp=maxVoltage=minVoltage;
  Irms=abs(1.9111*Vpp - 0.1);
  Serial.print("Irms =");
  Serial.print(Irms);
  Serial.println(" [A]");
  Serial.print("Consumo: ");
  Serial.print(220*Irms);
  Serial.println(" [VA]");
  Serial.println();
  delay(300);
}
