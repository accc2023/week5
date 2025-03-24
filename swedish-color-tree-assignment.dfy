// BEGIN-TODO(Name)
// Please, before you do anything else, add your names here:
// Group 69
// Jazman Mohamad Ismail: 1923072
// Arhan Chhabra: 1940198
//
// Good luck!
//
// END-TODO(Name)

datatype ColoredTree = Leaf(Color)
                     | Node(ColoredTree, ColoredTree)

datatype Color = Blue | Yellow | Green | Red

predicate IsSwedishFlagColor(c : Color)
{
  c.Blue? || c.Yellow?
}

// BEGIN-TODO(Extra)
// Space for extra functions and lemmas (optional)
// END-TODO(Extra)

predicate IsSwedishColoredTree(t: ColoredTree)
{
// BEGIN-TODO(IsSwedishColorTree)
// Implement the `IsSwedishColoredTree` predicate according to the instructions.
// END-TODO(IsSwedishColorTree)
}
