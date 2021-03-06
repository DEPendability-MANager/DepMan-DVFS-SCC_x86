#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/uio.h>
#include <sys/wait.h>
#include <fcntl.h> 
#include <signal.h>
#include "Voltage_Check.h"

// struct timeval ttstart,ttemp;

// char monitoring_command[1000]="sccBmc -c status | grep 3V3SCC >> monitor_3V3SCC.txt";
  char temp[1000];


void sigHandler(int signumber){

   gettimeofday(&ttemp,NULL);
   
   if(signumber == SIGUSR1) {
    printf("SIGUSR1 catched. PID=%d\n",getpid());
   }

sprintf(temp,"echo Change_Timestep= %lf>>monitor_3V3SCC.txt",(ttemp.tv_sec - ttstart.tv_sec) + (ttemp.tv_usec - ttstart.tv_usec) * 0.000001);
system(temp);	
	
	sprintf(monitoring_command,"i have changed it");
}

void monitor_voltages(){
   
    gettimeofday(&ttstart,NULL);
    while(1){
	system(monitoring_command);
	gettimeofday(&ttemp,NULL);	
	sprintf(temp,"echo command executed timestep= %lf>>monitor_3V3SCC.txt",(ttemp.tv_sec - ttstart.tv_sec) + (ttemp.tv_usec - ttstart.tv_usec) * 0.000001);
	system(temp);
    }
}



int main (int argc, char *argv[]){
    double voltage_change_overhead;
    double difference = 0.20;
    char command_buff[100];
    int res;

    struct timeval tts, ttf,ttinitf;	//measure total time of main

   
    printf("Welcome to main\n");

    pid_t monitor_process;

    monitor_process=fork();

if (monitor_process==0){
    signal(SIGUSR1 ,sigHandler);
    printf("calling monitoring\n");
    monitor_voltages();

}else{

    gettimeofday (&tts, NULL);

    init_voltage_files(); 
 
    gettimeofday (&ttinitf, NULL);

    kill(monitor_process,SIGUSR1);

    sprintf(command_buff,"./rccerun -nue 41 -f /shared/apostolis/brain/rc.hosts_41 FV %d",atoi(argv[1]));
    res=system(command_buff);
    
       voltage_change_overhead = voltage_check(difference);
//	printf("already forked going to sleep\n");
//	sleep(1);
//	printf("already send the signal\n");
	 gettimeofday (&ttf, NULL);
   
     printf("Time to init files= %lf\n",(ttinitf.tv_sec - tts.tv_sec) + (ttinitf.tv_usec - tts.tv_usec) * 0.000001);
      printf("Total time= %lf\n",(ttf.tv_sec - tts.tv_sec) + (ttf.tv_usec - tts.tv_usec) * 0.000001);
      printf("The voltage time result is= %lf\n",voltage_change_overhead);

	sprintf(command_buff,"echo Time to init files= %lf>>voltage_level_all.txt",(ttinitf.tv_sec - tts.tv_sec) + (ttinitf.tv_usec - tts.tv_usec) * 0.000001);
	system(command_buff);

	sprintf(command_buff,"echo Total time= %lf>>voltage_level_all.txt",(ttf.tv_sec - tts.tv_sec) + (ttf.tv_usec - tts.tv_usec) * 0.000001);
	system(command_buff);

	sprintf(command_buff,"echo The voltage time result= %lf>>voltage_level_all.txt",voltage_change_overhead);
	system(command_buff);
}
kill(monitor_process,SIGKILL);
return 0;
}
