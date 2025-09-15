(defun send-expression-to-server (expression)
  "Envía una expresión al servidor  muestra la respuesta."
  (interactive "sIngrese una expresión a evaluar: ")
  (let ((host "127.0.0.1")
        (port 65432)
        (response ""))
    ;; Crear un socket TCP/IP
    (with-temp-buffer
      (let ((process (open-network-stream "python-server" (current-buffer) host port)))
        (when process
          ;; Enviar la expresión al servidor
          (process-send-string process (concat expression "\n"))
          ;; Esperar la respuesta del servidor
          (accept-process-output process 2) ; Espera 2 segundos por la respuesta
          (setq response (buffer-string))
          (delete-process process)))
      ;; Mostrar la respuesta en el minibuffer
      (message "Respuesta del servidor: %s" response))))

;; ejemplo
(send-expression-to-server "t 5 >> t 7 >> & t * 11 >>")
