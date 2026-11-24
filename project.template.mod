// ** PLEASE ONLY CHANGE THIS FILE WHERE INDICATED **
// In particular, do not change the names of the OPL variables.

int N = ...; // #time steps 
int L = ...; // lower bound
int U = ...; // upper bound
int T = ...; // min proft

int P[1..N] = ...; // profit the machine makes in each timestemp 
int E[1..N] = ...; // energy cost in each timestamt

// Define here your decision variables and
// any other auxiliary OPL variables you need.
// You can run an execute block if needed.

//decision variable for each timestamp 
dvar boolean X[0..N+1]; 

// You can run an execute block if needed.

execute {

}

minimize sum(n in 1..N) E[n]*X[n];

subject to {

    X[0] == 0;
    X[N+1] == 0;

    // lower bound constraints
    forall(n in 1..N-L+1)
        sum(i in n..(n+L-1))
            X[i] >= L*(X[n]-X[n-1]);

    // min tail bound constraint
    forall(n in N-L+2..N)// this should be < than L
        sum(i in n..N)
            X[i] >= L*(X[n]-X[n-1]);

    // upper bound constraints
    forall(n in 1..N-U)
        sum(i in n..n+U) X[i] <= U;
 
    // minimum profit should be reached
    sum(n in 1..N) X[n]*P[n] >= T;
}

// You can run an execute block if needed.

execute {
//    forall (x in 0..N+L) 
//        print(X[x]);
}
