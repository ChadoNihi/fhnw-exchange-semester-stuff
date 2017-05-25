defmodule RSA do
  require Integer

  def find_d(n, _) when n < 1 or round(n) != n, do: raise ArgumentError, message: "n must be > 0 and an integer."
  def find_d(n, e) do # e,n and d,n are coprimes; e*d mod n == 1 mod n
    one_mod_n = rem(1, n)
    coprimes_n = Enum.reduce((n-1)..1, [], fn(cand, coprimes) ->
      if !(Integer.is_even(n) and Integer.is_even(cand)) and gcd(n, cand) == 1 do
        [cand | coprimes]
      else
        coprimes
      end
    end)

    unless Enum.member?(coprimes_n, e) do
      raise ArgumentError, message: "The 2nd arg, e, must be a coprime with n"
    else
      d = Enum.find(coprimes_n, false, &(rem(e*&1, n) == one_mod_n))
      d
    end
  end

  defp gcd(a, 0), do: a
  defp gcd(a, b), do: gcd(b, rem(a, b))
end

IO.puts RSA.find_d(44,5)
