// BEGIN-TODO(Name)
// Please, before you do anything else, add your names here:
// Group <Group number>
// <Full name 1>: <Student number 1>
// <Full name 2>: <Student number 2>
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
