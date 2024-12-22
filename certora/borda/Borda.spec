/*
* Verification of simple voting contract that uses Borda Election
*/


methods {
    function vote(address,address,address) external;
    function voted(address) external returns bool envfree;
    function points(address) external returns uint256 envfree;
    function winner() external returns address envfree;
}

rule user_marked_voted_after_voting(address f, address s, address t) {
    env e;
    vote(e, f, s, t);

    assert voted(e.msg.sender);
}

rule single_vote_per_user(address f, address s, address t) {
    env e;
    bool user_already_voted = voted(e.msg.sender);
    vote@withrevert(e, f, s, t);
    assert user_already_voted => lastReverted;
}

rule points_update_after_vote(address f, address s, address t) {
    env e;
    uint256 f_pts = points(f);
    uint256 s_pts = points(s);
    uint256 t_pts = points(t);
    vote(e, f, s, t);
    assert to_mathint(points(f)) == f_pts + 3;
    assert to_mathint(points(s)) == s_pts + 2;
    assert to_mathint(points(t)) == t_pts + 1;
}

invariant winner_has_highest_points(address x)
    points(winner()) >= points(x);