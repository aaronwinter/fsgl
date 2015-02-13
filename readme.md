# fsgl
#### by [Elvin Yung](https://github.com/elvinyung)
### Simple dynamically-typed functional(ish) programming language

### Setup
Make sure you have Python with version at least 3.4.1.

### Hello World
```
prints('Hello World!')
```

### Primitive Types
```
a = 5  ; integer
b = true  ; boolean
c = :something  ; symbol
d = 'a string of characters'  ; string

a = 5  ; ERROR, can't mutate variables
```

### Advanced Types
#### List
```
l = (1, 2, 3, 4)
head(l)  ; 1
tail(l)  ; (2, 3, 4)
```

#### Vector
```
v = [1, 2, 3, 4]
v(2)  ; 3
len(v)  ; 4
```

### Map
```
m = #{
  :a 4,
  'stringkey' :symbolvalue,
  true (6, 6, 6)
}

m(:a)  ; 4
m('stringkey')  ; :symbolvalue
m(true)  ; (6, 6, 6)
```

### Basic operations
```
a = 5
b = +(3, 5)  ; 8
c = -(1, 4, 8)  ; -11
d = /(2, 4, 10)  ;  frac(1, 20)
e = +(*(2, 5), 7)  ; 17
f = >(4, -1)  ; true
```

### Pattern matching
```
a, b = (1, 2, 3)  ; a = 1, b = (2, 3)
c, d, e = [4, 5, 6]  ; c = 4, d = 5, e = 6
```

### Functions
```
f = (x, y, z) => {
  +(x, *(y, z))
}

f(1, 2, 3)  ; 7
f(4, 5)  ; (z) var => { f(4, 5, z) }

g = { 4 + 5 }
g()  ; 9

(a) var => { 4 + a }(10)  ; 14
```

### Branching
```
a = if({ >(4, 5) }, 47, :no)  ; :no
```

### Higher Order Functions
```
map((x) var => {x+1}, [1, 2, 3])  ; [2, 3, 4]
foldl((a, b) var => )
```

### Basic I/O
```
prints('string')  ; 'string'
prints(65)  ; '17'
prints(true)  ; '1'
prints(:thing)  ; 'thing'

a = reads()
>>something
a  ; 'something'
```
