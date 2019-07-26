(ql:quickload (list :usocket :ulf-lib))

(defpackage :composition (:use :cl :usocket :ulf-lib))
(in-package :composition)

(defun read-to-string (stream)
  	(loop for char = (read-char-no-hang stream nil :eof)
    	until (or (null char) (eql char :eof)) collect char into msg
     	finally (return (values msg char))))

(defun split-by-one-space (string)
    (loop for i = 0 then (1+ j)
        as j = (position #\Space string :start i)
        collect (subseq string i j)
        while j))

(defun eval-expressions (string)
	(let* ((exps (mapcar #'read-from-string (split-by-one-space string)))
			(func (car exps))
			(args (cdr exps)))
		(apply func args)))
 
(defun run-server (port &optional (log-stream *standard-output*))
  (let ((connections (list (socket-listen "localhost" port :reuse-address t))))
    (unwind-protect
	 	(loop (loop for ready in (wait-for-input connections :ready-only t)
		  	do (if (typep ready 'stream-server-usocket)
			 	(push (socket-accept ready) connections)
			 	(let* ((stream (socket-stream ready))
						(msg (coerce (read-to-string stream) 'string)))
			   		(format log-stream (concatenate 'string "Received: (" msg ")"))
					(setq res (eval-expressions msg))
					(write-string (string res) stream)
			   		(socket-close ready)
			   		(setf connections (remove ready connections))))))
      	(loop for c in connections do (loop while (socket-close c))))))

(run-server 5432)