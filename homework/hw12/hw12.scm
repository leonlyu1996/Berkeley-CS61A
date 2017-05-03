(define (find s predicate)
  (if (null? s) #f 
      (if (predicate (car s)) (car s) (find (cdr-stream s) predicate)))
)

(define (scale-stream s k)
  (cons-stream (* (car s) k) (scale-stream (cdr-stream s) k))
)

(define (has-cycle s)
  (define (cycle? s t)
      (cond ((null? t) #f)
            ((eq? t s) #t)
            (else (cycle? s (cdr-stream t)))))
  (cycle? s (cdr-stream s))    
)

(define (has-cycle-constant s)
  (define (cycle? s t)
      (cond ((null? t) #f)
            ((eq? t s) #t)
            (else (cycle? s (cdr-stream t)))))
  (cycle? s (cdr-stream s)) 
)
