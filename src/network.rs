pub fn check_magic_number() {
    
}


//
pub fn tell_every_node_in_my_address_list_i_have_new_nn_outputs_to_send() {}


//
pub fn send_my_nn_outputs_to_remote_node() {
    
    /* 
    RELAY (OR NODE-IN-THE-MIDDLE) ATTACK:
    A sends its outputs to B. B changes A's outputs to
    look like they belong to B before sending them to C. When A
    releases its selected frames, B duplicates them and releases a
    copy but with their own signature

    The arborists assume B is the owner and pay B for A's work since B's signature is on every published output.


    RELAY (OR NODE-IN-THE-MIDDLE) ATTACK PREVENTION: A puts its public
    address (or signature) inside the message of each digest. And
    provides a signature to the entire output as well. Arborists slash
    anyone who puts their signature to the entire output but isn't
    inside the output's digest
    */
    
}


/*
DEAD END ATTACK:
Nodes don't relay other nodes outputs in order to conserve bandwidth

DEAD END ATTACK SEMI-PREVENTION:
A node that only relays its own data becomes very identifiable. 
*/

/* 
NOTHING TO LOSE NOOBS ATTACK:
A new node has no coins presumably so it cannot be slashed. It can perform a NITM attack or DE attack with no reprecussions

NOTHING TO LOSE NOOBS ATTACK PREVENTED: If a node's public key isn't
in the public key list in the database, which all nodes must keep,
incumbent nodes give frames to nodes with no coins in order for them
to perform proof-of-work before they'll relay their outputs. Once a node is added to the Merkle Tree, it's added to the public key list
*/


//
pub fn check_if_i_have_frame_hashes_other_node_is_telling_me_they_have() {}

//
pub fn if_i_dont_have_frame_hashes_ask_node_to_send_me_data() {}



/* How do I make it so that there is sufficient competition to be an arborist.

Any node can be an arborist. There could be a situation where every node is an arborist. That's not good. 

We want more nodes than arborists. So we want arborists to be a small percentage of the nodes.

If I set the arborists_commission too high, nodes will stop being nodes and become arborists because it's worth more. As the number of nodes drop, the commission will drop but I'll get more people wanting to be an arborist. So it can't be too easy to be an arborist.


If arborists only have to do 5 frames, then below a certain number of nodes, it's much easier to be an arborist than a node, if arborists always make a certain percentage.


SOLUTION: The arborist can get paid in transaction fees. Market forces
will ensure that there's always an arborist and that it's always worth
it.

 
*/
// pub const arborists_commission: u32; 




pub fn check_if_new_calibration() {
    // Node checks if any data is for a calibration not in their memory (it won't be if it wasn't in any of the previous blocks in the chain)
    
}


// check if this node has skin in the game to prevent from being spammed
pub fn check_if_this_node_has_been_in_a_block() {}
