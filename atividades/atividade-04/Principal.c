#include <stdio.h>
#include <windows.h>
//#include <unistd.h>

// Código feito por Mateus A.
// Basicamente um sistema de relógio

int main(){

	int horas, minutos, segundos = 0;
	int delay = 1000;
	
	printf("Insira a hora atual no formato HH:MM\n");
	scanf("%d%d", &horas, &minutos);
	
	if(horas > 24 || minutos > 60){
		printf("Erro!");
		return -1;
	}
	
	while(1){
		
		segundos++;
		
		if(segundos == 60){
			segundos = 0;
			minutos++;
		}
		
		if(minutos == 60){
			minutos = 0;
			horas++;
		}
		
		if(horas > 12){
			horas = 1;
		}
		
		
		printf("Hora atual: %d:%d:%d\n", horas, minutos, segundos);
		system("cls");
		sleep(delay);
		
		
	}
	
	
	getchar();


	return 0;
}
