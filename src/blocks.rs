

mod checking_the_block {
    //
    pub fn check_arborists_block() {}

    pub fn check_if_block_has_more_nodes_than_last_accepted_block() {}

    //
    pub fn check_block_if_my_coinbase_data_and_reserved_digests_are_in_block() {}

    //
    pub fn check_blocks_frame_activations_for_random_frames_from_other_nodes() {}

}

mod building_the_block {
    // must be checked before other tests
    pub fn arborist_check_they_have_all_the_data_they_need_for_this_node_from_the_past_ten_minutes() {}

    //
    pub fn arborist_checks_if_no_data_in_block_contradicts_other_data() {}


    //
    pub fn arborist_unlocks_each_nodes_cptsh_or_cptpkh() {

        // THE COINBASE-PAY-TO-PUBLIC-KEY-HASH NEVER LEAVES THE COINS AT THE ADDRESS OF THE COINBASE-PUBLIC-KEY. THEY MUST BE IMMEDIATELY TRANSFERRED TO AN ACTUAL PRIVATELY CONTROLLED ADDRESS SINCE THE COINBASE PRIVATE KEY IS THE htcoardt IT CAN BE DISCOVERED BY ANYONE WHO COMPUTES THE FRAMES. 

        // The arborist creates an unlocking script that includes a signature that matches the public key of the coinbase-pay-to-public-key-hash (The private key for which is the htcoardt) and which pays the node_coinbase_split to the address the node specified and pays the arborists_coinbase_split to an address the arborist themselves specify. Then they sign that



    }

    //
    pub fn arborist_writes_coinbase_transaction_for_all_nodes_in_block() {


    }

}



