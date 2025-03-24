// BEGIN-TODO(Name)
// Please, before you do anything else, add your names here:
// Group <Group number>
// <Full name 1>: <Student number 1>
// <Full name 2>: <Student number 2>
//
// Good luck!
//
// END-TODO(Name)

datatype Expr =
  True 
  | False
  | Var(s: string)
  | Not(arg: Expr) 
  | And(left: Expr, right: Expr)
  | Or(left: Expr, right: Expr)
  | Implies(left: Expr, right: Expr)

// BEGIN-TODO(Extra)
// Space for extra functions and lemmas (optional)
// END-TODO(Extra)

predicate Eval(x: Expr, env: map<string, bool>)
{
// BEGIN-TODO(Eval)
// Implement the `Eval` predicate according to the instructions.
// END-TODO(Eval)
}

method TestEval()
{
  var env := map["a" := true, "b" := false, "c" := true];
  assert Eval(And(True, True), env) == true;
  assert Eval(Implies(Var("a"), False), env) == false;
}

function Simplify(x: Expr): Expr
// BEGIN-TODO(Simplify)
// Implement the `Simplify` function according to the instructions.
// END-TODO(Simplify)

method TestSimplify()
{
// BEGIN-TODO(TestSimplify)
// Insert your test cases for the `Simplify` function.
// END-TODO(TestSimplify)
}
