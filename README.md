# RedRobin Quick Reference

Lenguaje básico orientado a objetos.

## Condicionales

### If/Else

```
  if (condicion or condicion) {
    accions;
  }
  else {
    accions;
  }
```

### Elif

```
  if (condicion) {
    acciones;
  } elif (condicion) {
    acciones;
  }
  else {
    acciones;
  }
```

## Ciclos

### For

```
  for i in (LimInf _ LimSup) step n {
    acciones;
  }
```
NOTA: la variable de control i debe estar previamente declarada

### While

```
  while (condiciones) {
    acciones;
  }
```

## Funciones

```
  func public empty funcion1(number: i, j; real k) {
    acciones;
    give i + j + k;
  }
```
Una función puede ser public o secret

### Envio de arreglos y parametros por referencia

```
  func secret empty funcion2(number[]: i; number k) {
    acciones;
  }
  
  funcion2(v, &p);
```

## Clases

```
  class foo inherit foop {
    public number n;
    secret boolean b;
    secreto foop f;
    ...
    
    func public empty funcion() {
      acciones;
    }
  }
```

## Esturcutra general

```
class RedRobin {
  RedRobin() {
    string nombre;
    read(nombre);
    print("Hola " + nombre);
  }
}
```

## Funciones de casteo

```
  toString(s)
  toReal(s)
  toNumber(s)
```
