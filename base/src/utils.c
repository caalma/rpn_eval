#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include <time.h>

void save_last_t(int t, const char *filename) {
    FILE *file = fopen(filename, "w");
    if (file == NULL) {
        perror("Error al abrir el archivo para guardar t");
        return;
    }
    fprintf(file, "%d", t);
    fclose(file);
}

void sleep_for_rate(int rate) {
    struct timespec ts;
    ts.tv_sec = 0;
    ts.tv_nsec = 1000000000L / rate; // Nanosegundos por muestra
    nanosleep(&ts, NULL);
}

void sleep_for_rate_gt(int rate) {
    struct timespec start_time, end_time;
    long nanoseconds_per_sample = 1000000000L / rate; // Nanosegundos por muestra

    // Obtener el tiempo actual
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    // Calcular el tiempo de finalización
    end_time.tv_sec = start_time.tv_sec + (start_time.tv_nsec + nanoseconds_per_sample) / 1000000000L;
    end_time.tv_nsec = (start_time.tv_nsec + nanoseconds_per_sample) % 1000000000L;

    // Esperar hasta que se alcance el tiempo de finalización
    while (1) {
        struct timespec current_time;
        clock_gettime(CLOCK_MONOTONIC, &current_time);

        // Comprobar si hemos alcanzado o superado el tiempo de finalización
        if ((current_time.tv_sec > end_time.tv_sec) ||
            (current_time.tv_sec == end_time.tv_sec && current_time.tv_nsec >= end_time.tv_nsec)) {
            break;
        }

        // Dormir brevemente para evitar un uso excesivo de CPU
        struct timespec sleep_time = {0, 100000}; // 100 microsegundos
        nanosleep(&sleep_time, NULL);
    }
}
