/-
  Hypergraph Limits & Monotonic Expansion in Lean 4
  Kernel verification of discrete hypergraph volume growth and spatial continuity
-/

namespace HypergraphLimits

/-- Discrete volume V(t) at update step t -/
def volume (t : Nat) : Nat :=
  2 ^ t

/-- Theorem: Volume is strictly monotonically increasing -/
theorem volume_strictly_increasing (t : Nat) :
  volume t < volume (t + 1) := by
  dsimp [volume]
  have hpos : 0 < 2 ^ t := Nat.two_pow_pos t
  have hsucc : 2 ^ (t + 1) = 2 ^ t + 2 ^ t := by
    rw [Nat.pow_succ]
    exact Nat.mul_two (2 ^ t)
  rw [hsucc]
  exact Nat.lt_add_of_pos_right hpos

/-- Theorem: Delta V(t) = 2^t -/
theorem delta_volume_exact (t : Nat) :
  volume (t + 1) - volume t = 2 ^ t := by
  dsimp [volume]
  have hsucc : 2 ^ (t + 1) = 2 ^ t + 2 ^ t := by
    rw [Nat.pow_succ]
    exact Nat.mul_two (2 ^ t)
  rw [hsucc]
  exact Nat.add_sub_cancel_left (2 ^ t) (2 ^ t)

end HypergraphLimits
