#[allow(non_snake_case)]
struct Problem{
    N: usize,
    L: usize,
    U: usize,
    T: usize,
    P:Vec<usize>,
    E:Vec<usize>,
}
#[allow(non_snake_case)]
impl Problem{
    fn new(N:usize, L:usize, U:usize, 
        T:usize, P:Vec<usize>, E:Vec<usize>)->Problem{
        assert!(L>=1,"L is greater than or equal to 1");
        assert!(U>=L,"U is greater than or equal to L");
        assert!(N>=U,"N is greater than or equal to U");
        Problem {N,L,U,T,P,E}
        // Minimize E, while arriving to minimum profit T
        // Always choose minimum E. 
        // Always choose best Profit per energy comsuption.
        // T = 10
        // P = [1 1 10]
        // E = [1 2 8]
    }
    fn solve(&self){
        let mut profit: usize = 0;
        let mut solution: Vec<bool>= vec![false;self.N];
        let mut profit_efficiency: Vec<(f64, usize)> = Vec::new();
        let mut continuous_groups: Vec<isize> = vec![-1;self.N];
        for i in 0..self.N{
            profit_efficiency.push((self.P[i] as f64/self.E[i] as f64 + 1f64, i));
        }
        profit_efficiency.sort_by(|a,b|b.0.total_cmp(&a.0));
        for e in profit_efficiency{
            if solution[e.1] {
                continue;
            }else {
                let left = continuous_groups.get(e.1 - 1);
                let right = continuous_groups.get(e.1 + 1);
                
                match (left, right) {
                    (Some(l),None)=>{

                    },
                    (None,Some(r))=>(),
                    (Some(l),Some(r))=>(),
                    (None, None)=>(),
                    _ =>(), 
                }
                solution[e.1] = true;
                profit += self.P[e.1];

            }
            if profit >= self.T {
                break;
            }
        }
    }
}
fn main() {
    println!("Hello, world!");
}
