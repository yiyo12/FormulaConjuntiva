import re
import sys

class Atomo:
    def __init__(self,nombre):
        self.nombre=nombre
        self.negado=False
        
    def notAtomo(self):
        self.negado=not(self.negado)
        
    def getClon(self):
        clon = Atomo(self.nombre)
        clon.negado = self.negado
        return clon
    
    def toString(self):
        if(self.negado):
            return '~'+self.nombre
        return self.nombre

class Clausula:
    def __init__(self):
        self.atomos=[]
    
    def addAtomo(self, atomo):
        self.atomos.append(atomo)
        
    def getClon(self):
        c = Clausula()
        for a in self.atomos:
            c.addAtomo(a.getClon())
        return c

    def notClausula(self):
        f = Formula()
        for a in self.atomos:
            b = a.getClon()
            b.notAtomo()
            c = Clausula()
            c.addAtomo(b)
            f.addClausula(c)
        return f

    def toString(self):
        cad = '( '
        for a in self.atomos:
            cad += a.toString()+ ' , '
        if (len(self.atomos) == 0):
            cad = '( )'
        else:
            cad = cad[:-2]+')'
        return cad

class Formula:
    def __init__(self):
        self.clausulas=[]
        self.certificado={}
    
    def addClausula(self,clausula):
        self.clausulas.append(clausula)
        
    def andFormula(self,formula):
        f = Formula()
        for c in self.clausulas:
            f.addClausula(c)
        for c in formula.clausulas:
            f.addClausula(c)
        return f
    
    def notFormula(self):
        f = Formula()
        for c in self.clausulas:
            g = c.notClausula()
            f = f.orFormula(g)
        return f
    
    def orFormula(self,formula):
        f = Formula()
        g = []
        for c in formula.clausulas:
            g.append(self.orClausula(c))
        for h in g:
            for c in h.clausulas:
                f.addClausula(c)
        return f
    
    def orClausula(self,clausula):
        f = Formula()
        if(len(self.clausulas)==0):
            f.addClausula(clausula.getClon())
            return f
        for c in self.clausulas:
            x = c.getClon()
            for a in clausula.atomos:
                x.addAtomo(a.getClon())
            f.addClausula(x)
        return f
    
    def toString(self):
        cad='[ '
        for c in self.clausulas:
            cad += c.toString() + ' '
        if (len(self.clausulas) == 0):
            cad = '[ ],{ '
        else:
            cad = cad[:-2]+'],{ '
        for a in self.certificado.keys():
            b = Atomo.Atomo(a)
            if(self.certificado[a]==True):
                b.notAtomo()
            cad += b.toString()+' '
        cad += '}'
        return cad
    
    
def getPrioridad(a):
    if(a == '|'):
        return 1
    if(a == '&'):
        return 2
    if(a == '>'):
        return 3
    if(a == '='):
        return 4
    if(a == '~'):
        return 5
    return 0

def infijo2postfijo(infijo):
    '''
    Entrada:    infijo es una lista de string,
                donde cada string es un operador u operando
    Salida:    postfijo, es una lista de string,
                donde cada string es un operador u operando, pero en 
                formato postfijo
    '''
    postfijo = []
    pila = []
    for ch in infijo:
        if(ch == '('):
            pila.append(ch)
        elif(ch == ')'):
            while(len(pila)>0):
                tope=pila.pop()
                if(tope != '('):
                    postfijo.append(tope)
                else:
                    break
        elif(ch.isalnum()):
            postfijo.append(ch)
        else:
            if(len(pila)==0 or getPrioridad(ch) > getPrioridad(pila[-1])):
                pila.append(ch)
            else:
                while(len(pila)>0 and getPrioridad(ch) < getPrioridad(pila[-1])):
                    tope=pila.pop()
                    postfijo.append(tope)
                pila.append(ch)
    while(len(pila)>0):
        postfijo.append(pila.pop())
    return postfijo
    
def evaluar(posfijo):
    pila=[]
    for ch in postfijo:
        if(ch.isalnum()):
            f=Formula()
            c=Clausula()
            a=Atomo(ch)
            c.addAtomo(a)
            f.addClausula(c)
            pila.append(f)
        else:
            if(ch == '|'):
                b = pila.pop()
                a = pila.pop()
                c = a.orFormula(b)
            elif(ch == '&'):
                b = pila.pop()
                a = pila.pop()
                c = a.andFormula(b)
            elif(ch == '>'):
                b = pila.pop()
                a = pila.pop()
                a = a.notFormula()
                c = a.orFormula(b)
            elif(ch == '='):
                b = pila.pop()
                a = pila.pop()
                d = a.notFormula()
                e = b.notFormula()
                f = d.orFormula(b)
                g = e.orFormula(a)
                c = f.andFormula(g)
            elif(ch == '~'):
                a = pila.pop()
                c = a.notFormula()
            pila.append(c)
    return pila.pop()

archivo = open("formulas.txt")
formulas = archivo.readlines()
formula = 32
infijo= re.findall('(\w+|\||\&|\>|\=|\~|\(|\))', formulas[formula])
postfijo= infijo2postfijo(infijo)
print('\ninfijo String:\n',formulas[formula])
print('infijo Lista:\n',infijo)
print('postfijo Lista:\n',postfijo)

resultado = evaluar(postfijo)
print('FNC: \n',resultado.toString())
