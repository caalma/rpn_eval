(defun send-expression-via-client (expression)
  "Envía una expresión al servidor Python usando un script cliente externo."
  (interactive "sIngrese una expresión a evaluar: ")
  (let ((script-path "../python/directo.py") ; Cambia esto a la ruta de tu script
        (response ""))
    ;; Ejecutar el script cliente y capturar la salida
    (setq response (shell-command-to-string (concat script-path " \"" expression "\"")))
    ;; Mostrar la respuesta en el minibuffer
    (message "Respuesta del servidor: %s" response)))


(send-expression-via-client "t 3 / t 7 / & ")
