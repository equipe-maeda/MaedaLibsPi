void levar_1(){
    int p = 0;
    digitalWrite(17, 1);
    for(p = 0; p < 200; p++){
        digitalWrite(13, 1);
        delay(20);
        digitalWrite(13, 0);
    }

       digitalWrite(18, 1);
        for(p = 0; p < 50; p++){
        digitalWrite(14, 1);
        delay(20);
        digitalWrite(14, 0);
    }

}