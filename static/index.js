// document.addEventListener(
//     'DOMContentLoaded', 
//     check_connection_change_interface(), 
//     false
//   );


async function test(){
    console.log("test!!");
}

async function save_code(){
    document.getElementById('code-form').submit();
    console.log("submitted");
}

async function delete_code(){
    document.getElementById('delete-form').submit();
    console.log("deleted");
}

async function ast_table(){
    document.getElementById('ast-form').submit();
    console.log("ast table created");
}

async function flatcode_table(){
    document.getElementById('flatcode-form').submit();
    console.log("flatcode table created");
}

async function abc_matrix(){
    document.getElementById('abc-matrix-form').submit();
    console.log("abc matrix created");
}

async function put_values(){
    document.getElementById('put-values-form').submit();
    console.log("retrieve inputs");
}

async function calculate_r_values(){
    document.getElementById('calculate-r-form').submit();
    console.log("calculate r");
}

async function create_qap(){
    document.getElementById('create-qap-form').submit();
    console.log("create qap");
}

async function create_qap_lcm(){
    document.getElementById('create-qap-lcm-form').submit();
    console.log("create qap lcm");
}

async function create_qap_fr(){
    document.getElementById('create-qap-fr-form').submit();
    console.log("create qap fr");
}

async function random_toxic(){
    let maxValue = 999999999999;

    let alpha = Math.floor(Math.random() * maxValue);
    let beta = Math.floor(Math.random() * maxValue);
    let delta = Math.floor(Math.random() * maxValue);
    let gamma = Math.floor(Math.random() * maxValue);
    let x_val = Math.floor(Math.random() * maxValue);
    
    let toxic_alpha = document.getElementsByName('toxic-alpha')[0]
    let toxic_beta = document.getElementsByName('toxic-beta')[0]
    let toxic_delta = document.getElementsByName('toxic-delta')[0]
    let toxic_gamma = document.getElementsByName('toxic-gamma')[0]
    let toxic_x_val = document.getElementsByName('toxic-x-val')[0]

    toxic_alpha.value = alpha;
    toxic_beta.value = beta;
    toxic_delta.value = delta;
    toxic_gamma.value =  gamma;
    toxic_x_val.value = x_val;
}

async function random_toxic_clear(){
    let toxic_alpha = document.getElementsByName('toxic-alpha')[0]
    let toxic_beta = document.getElementsByName('toxic-beta')[0]
    let toxic_delta = document.getElementsByName('toxic-delta')[0]
    let toxic_gamma = document.getElementsByName('toxic-gamma')[0]
    let toxic_x_val = document.getElementsByName('toxic-x-val')[0]

    toxic_alpha.value = null;
    toxic_beta.value = null;
    toxic_delta.value = null;
    toxic_gamma.value = null;
    toxic_x_val.value = null;

    toxic_alpha.setAttribute('placeholder', 'alpha');
    toxic_beta.setAttribute('placeholder', 'beta');
    toxic_delta.setAttribute('placeholder', 'delta');
    toxic_gamma.setAttribute('placeholder', 'gamma');
    toxic_x_val.setAttribute('placeholder', 'x_val');
    
    clear_toxic();
}

async function save_toxic(){
    document.getElementById('save-toxic-form').submit();
    console.log("toxic form submitted");
}

async function clear_toxic(){
    document.getElementById('clear-toxic').submit();
}

async function retrieve_polys(){
    document.getElementById('retrieve-poly-form').submit();
}

async function calc_polys_evaluation(){
    document.getElementById('calc-polys-evaluation').submit();
}