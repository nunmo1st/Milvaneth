window.onload = function() {
  var buyer_World;
  var buyer_Datacenter;
  var seller_World;
  var seller_Datacenter;
  buyer_World = document.getElementById("buyer_World");
  buyer_Datacenter = document.getElementById("buyer_Datacenter");
  buyer_Datacenter.onchange = change_buyer_Datacenter;

  seller_World = document.getElementById("seller_World");
  seller_Datacenter = document.getElementById("seller_Datacenter");
  seller_Datacenter.onchange = change_seller_Datacenter;
}


function change_buyer_Datacenter() {
  var changed_buyer_DC = document.getElementById("buyer_Datacenter").value;

  if (changed_buyer_DC == "Elemental") {
    set_buyer_Elemental();
  } else if (changed_buyer_DC == "Gaia") {
    set_buyer_Gaia();
  } else if (changed_buyer_DC == "Mana") {
    set_buyer_Mana();
  } else if (changed_buyer_DC == "Meteor") {
    set_buyer_Meteor();
  } else if (changed_buyer_DC == "Aether") {
    set_buyer_Aether();
  } else if (changed_buyer_DC == "Crystal") {
    set_buyer_Crystal();
  } else if (changed_buyer_DC == "Dynamis") {
    set_buyer_Dynamis();
  } else if (changed_buyer_DC == "Primal") {
    set_buyer_Primal();
  } else if (changed_buyer_DC == "Chaos") {
    set_buyer_Chaos();
  } else if (changed_buyer_DC == "Light") {
    set_buyer_Light();
  } else if (changed_buyer_DC == "Materia") {
    set_buyer_Materia();
  } else {
    set_buyer_Null();
  }
}

function change_seller_Datacenter() {
  var changed_seller_DC = document.getElementById("seller_Datacenter").value;

  if (changed_seller_DC == "Elemental") {
    set_seller_Elemental(seller_World);  // seller_Worldを引数として渡す
  } else if (changed_seller_DC == "Gaia") {
    set_seller_Gaia(seller_World);
  } else if (changed_seller_DC == "Mana") {
    set_seller_Mana(seller_World);
  } else if (changed_seller_DC == "Meteor") {
    set_seller_Meteor(seller_World);
  } else if (changed_seller_DC == "Aether") {
    set_seller_Aether(seller_World);
  } else if (changed_seller_DC == "Crystal") {
    set_seller_Crystal(seller_World);
  } else if (changed_seller_DC == "Dynamis") {
    set_seller_Dynamis(seller_World);
  } else if (changed_seller_DC == "Primal") {
    set_seller_Primal(seller_World);
  } else if (changed_seller_DC == "Chaos") {
    set_seller_Chaos(seller_World);
  } else if (changed_seller_DC == "Light") {
    set_seller_Light(seller_World);
  } else if (changed_seller_DC == "Materia") {
    set_seller_Materia(seller_World);
  } else {
    set_seller_Null(seller_World);
  }
}

function set_buyer_Elemental() {
  buyer_World.textContent = null;

  var Elemental = [
    { cd: "", label: "ホームを選択して下さい" },
    { cd: "aegis", label: "Aegis" },
    { cd: "atomos", label: "Atomos" },
    { cd: "carbuncle", label: "Carbuncle" },
    { cd: "garuda", label: "Garuda" },
    { cd: "gungnir", label: "GunGnir" },
    { cd: "kujata", label: "Kujata" },
    { cd: "tonberry", label: "Tonberry" },
    { cd: "typhon", label: "Typhon" },
    { cd: "All" , label:"All"}
  ];

  Elemental.forEach(function(value) {
    var op = document.createElement("option");
    op.value = value.cd;
    op.text = value.label;
    buyer_World.appendChild(op);
  });
}


  function set_buyer_Gaia() {
      buyer_World.textContent = null;

    var Gaia = [
      {cd:"", label:"ホームを選択して下さい"},
      {cd:"alexander", label:"Alexander"},
      {cd:"bahamut", label:"Bahamut"},
      {cd:"durandal", label:"Durandal"},
      {cd:"fenrir", label:"Fenrir"},
      {cd:"ifrit", label:"Ifrit"},
      {cd:"ridill", label:"Ridill"},
      {cd:"tiamat", label:"Tiamat"},
      {cd:"ultima", label:"Ultima"},
      { cd: "All" , label:"All"}
    ];
  
    Gaia.forEach(function(value) {
  
      var op = document.createElement("option");
  
      op.value = value.cd;
  
      op.text = value.label;
  
      buyer_World.appendChild(op);
  
    });
  
  }

  function set_buyer_Mana() {
  
      buyer_World.textContent = null;
  
    var Mana = [  
      {cd:"", label:"ホームを選択して下さい"},
      {cd:"anima", label:"Anima"},
      {cd:"asura", label:"Asura"},
      {cd:"chocobo", label:"Chocobo"},
      {cd:"hades", label:"hades"},
      {cd:"ixion", label:"Ixion"},
      {cd:"masamune", label:"Masamune"},      {cd:"anima", label:"Anima"},
      {cd:"pandaemonium", label:"Pandaemonium"},
      {cd:"taitan", label:"Taitan"},
      { cd: "All" , label:"All"}
    ];
  
    Mana.forEach(function(value) {
  
      var op = document.createElement("option");
  
      op.value = value.cd;
  
      op.text = value.label;
  
      buyer_World.appendChild(op);
  
    });
  
  }

  function set_buyer_Meteor() {
  
    buyer_World.textContent = null
  
    var Meteor = [  
      {cd:"", label:"ホームを選択して下さい"},
      {cd:"belias", label:"Belias"},
      {cd:"mandragora", label:"Mandragora"},
      {cd:"ramuh", label:"Ramuh"},
      {cd:"shinryu", label:"Shinryu"},
      {cd:"unicorn", label:"Unicorn"},
      {cd:"valefor", label:"Valefor"},      {cd:"anima", label:"Anima"},
      {cd:"youjimbo", label:"Yojimbo"},
      {cd:"zeromus", label:"Zeromus"},
      { cd: "All" , label:"All"}
    ];
  
    Meteor.forEach(function(value) {
  
      var op = document.createElement("option");
  
      op.value = value.cd;
  
      op.text = value.label;
  
      buyer_World.appendChild(op);
  
    });

  }

  function set_buyer_Aether() {
  
      buyer_World.textContent = null;
  
    var Aether = [  
      {cd:"", label:"ホームを選択して下さい"},
      {cd:"adamantoise", label:"Adamantoise"},
      {cd:"cactuar", label:"Cactuar"},
      {cd:"faerie", label:"Faerie"},
      {cd:"gilgamesh", label:"Gilgamesh"},
      {cd:"jenova", label:"Jenova"},
      {cd:"midgardsormr", label:"Midgardsormr"},
      {cd:"Sargatanas", label:"Sargatanas"},
      {cd:"siren", label:"Siren"},
      { cd: "All" , label:"All"}
    ];
  
    Aether.forEach(function(value) {
  
      var op = document.createElement("option");
  
      op.value = value.cd;
  
      op.text = value.label;
  
      buyer_World.appendChild(op);
  
    });
  
  }
  function set_buyer_Crystal() {
  
      buyer_World.textContent = null;
  
    var Crystal = [  
      {cd:"", label:"ホームを選択して下さい"},
      {cd:"balmung", label:"Balmung"},
      {cd:"brynhildr", label:"Brynhildr"},
      {cd:"coeurl", label:"Coeurl"},
      {cd:"diabolos", label:"Diabolos"},
      {cd:"goblin", label:"Goblin"},
      {cd:"malboro", label:"Malboro"},
      {cd:"mateus", label:"Mateus"},
      {cd:"zalera", label:"Zalera"},
      { cd: "All" , label:"All"}
    ];
  
    Crystal.forEach(function(value) {
  
      var op = document.createElement("option");
  
      op.value = value.cd;
  
      op.text = value.label;
  
      buyer_World.appendChild(op);
  
    });
  }

  function set_buyer_Dynamis() {
  
      buyer_World.textContent = null;
  
    var Dynamis = [  
      {cd:"", label:"ホームを選択して下さい"},
      {cd:"halicarnassus", label:"halicarnassus"},
      {cd:"maduin", label:"Maduin"},
      {cd:"marilith", label:"Marilith"},
      {cd:"Seraph", label:"Seraph"},
      { cd: "All" , label:"All"}
    ];
  
    Dynamis.forEach(function(value) {
  
      var op = document.createElement("option");
  
      op.value = value.cd;
  
      op.text = value.label;
  
      buyer_World.appendChild(op);
  
    });
  
  }

  function set_buyer_Primal() {
  
      buyer_World.textContent = null;
  
    var Primal = [  
      {cd:"", label:"ホームを選択して下さい"},
      {cd:"behemoth", label:"Behemoth"},
      {cd:"excalibur", label:"excalibur"},
      {cd:"exodus", label:"Exodus"},
      {cd:"famfrit", label:"Famfrit"},
      {cd:"hyperion", label:"Hyperion"},
      {cd:"lamia", label:"Lamia"},
      {cd:"leviathan", label:"Leviathan"},
      {cd:"ultros", label:"Ultros"},
      { cd: "All" , label:"All"}
    ];
  
    Primal.forEach(function(value) {
  
      var op = document.createElement("option");

      op.value = value.cd;
  
      op.text = value.label;
  
      buyer_World.appendChild(op);
  
    });
  }

  function set_buyer_Chaos() {
  
      buyer_World.textContent = null;
  
    var Chaos = [  
      {cd:"", label:"ホームを選択して下さい"},
      {cd:"cerberus", label:"cerberus"},
      {cd:"louisoix", label:"louisoix"},
      {cd:"moogle", label:"Moogle"},
      {cd:"omega", label:"Omega"},
      {cd:"phantom", label:"Phantom"},
      {cd:"ragnarok", label:"Ragnarok"},
      {cd:"sagittarius", label:"Sagittarius"},
      {cd:"spriggan", label:"Spriggan"},
      { cd: "All" , label:"All"}
    ];
  
    Chaos.forEach(function(value) {
  
      var op = document.createElement("option");
      
      op.value = value.cd;
  
      op.text = value.label;
  
      buyer_World.appendChild(op);
  
    });
  }

  function set_buyer_Light() {
  
      buyer_World.textContent = null;
  
    var Light = [  
      {cd:"", label:"ホームを選択して下さい"},
      {cd:"alpha", label:"Alpha"},
      {cd:"lich", label:"Lich"},
      {cd:"odin", label:"Odin"},
      {cd:"phoenix", label:"Phoenix"},
      {cd:"raiden", label:"Raiden"},
      {cd:"shiva", label:"Shiva"},
      {cd:"twintania", label:"Twintania"},
      {cd:"zodiark", label:"Zodiark"},
      { cd: "All" , label:"All"}
    ];
  
    Light.forEach(function(value) {
  
      var op = document.createElement("option");
      
      op.value = value.cd;
  
      op.text = value.label;
  
      buyer_World.appendChild(op);
  
    });
  }

  function set_buyer_Materia() {
  
      buyer_World.textContent = null;
  
    var Materia = [ 
      {cd:"", label:"ホームを選択して下さい"},
      {cd:"bismarck", label:"Bismarck"},
      {cd:"ravana", label:"Ravana"},
      {cd:"Sephirot", label:"Sephirot"},
      {cd:"sophia", label:"Sophia"},
      {cd:"zurvan", label:"Zuruvan"},
      { cd: "All" , label:"All"}
    ];
  
    Materia.forEach(function(value) {
  
      var op = document.createElement("option");
      
      op.value = value.cd;
  
      op.text = value.label;
  
      buyer_World.appendChild(op);
  
    });
  }

  function set_buyer_Null() {
  
      buyer_World.textContent = null;
  
    var Null = [ 
      {cd:"", label:"ホームを選択して下さい"}
    ];
  
    Null.forEach(function(value) {
  
      var op = document.createElement("option");
      
      op.value = value.cd;
  
      op.text = value.label;
  
      buyer_World.appendChild(op);
  
    });
  }



// buyer↑
// seller↓




  function set_seller_Elemental() {
  seller_World.textContent = null;

  var Elemental = [
    { cd: "", label: "ホームを選択して下さい" },
    { cd: "aegis", label: "Aegis" },
    { cd: "atomos", label: "Atomos" },
    { cd: "carbuncle", label: "Carbuncle" },
    { cd: "garuda", label: "Garuda" },
    { cd: "gungnir", label: "GunGnir" },
    { cd: "kujata", label: "Kujata" },
    { cd: "tonberry", label: "Tonberry" },
    { cd: "typhon", label: "Typhon" }
  ];

  Elemental.forEach(function(value) {
    var op = document.createElement("option");
    op.value = value.cd;
    op.text = value.label;
    seller_World.appendChild(op);
  });
}


  function set_seller_Gaia() {
      seller_World.textContent = null;

    var Gaia = [
      {cd:"", label:"ホームを選択して下さい"},
      {cd:"alexander", label:"Alexander"},
      {cd:"bahamut", label:"Bahamut"},
      {cd:"durandal", label:"Durandal"},
      {cd:"fenrir", label:"Fenrir"},
      {cd:"ifrit", label:"Ifrit"},
      {cd:"ridill", label:"Ridill"},
      {cd:"tiamat", label:"Tiamat"},
      {cd:"ultima", label:"Ultima"}
    ];
  
    Gaia.forEach(function(value) {
  
      var op = document.createElement("option");
  
      op.value = value.cd;
  
      op.text = value.label;
  
      seller_World.appendChild(op);
  
    });
  
  }

  function set_seller_Mana() {
  
      seller_World.textContent = null;
  
    var Mana = [  
      {cd:"", label:"ホームを選択して下さい"},
      {cd:"anima", label:"Anima"},
      {cd:"asura", label:"Asura"},
      {cd:"chocobo", label:"Chocobo"},
      {cd:"hades", label:"hades"},
      {cd:"ixion", label:"Ixion"},
      {cd:"masamune", label:"Masamune"},      {cd:"anima", label:"Anima"},
      {cd:"pandaemonium", label:"Pandaemonium"},
      {cd:"taitan", label:"Taitan"},
    ];
  
    Mana.forEach(function(value) {
  
      var op = document.createElement("option");
  
      op.value = value.cd;
  
      op.text = value.label;
  
      seller_World.appendChild(op);
  
    });
  
  }

  function set_seller_Meteor() {
  
    seller_World.textContent = null
  
    var Meteor = [  
      {cd:"", label:"ホームを選択して下さい"},
      {cd:"belias", label:"Belias"},
      {cd:"mandragora", label:"Mandragora"},
      {cd:"ramuh", label:"Ramuh"},
      {cd:"shinryu", label:"Shinryu"},
      {cd:"unicorn", label:"Unicorn"},
      {cd:"valefor", label:"Valefor"},      {cd:"anima", label:"Anima"},
      {cd:"youjimbo", label:"Yojimbo"},
      {cd:"zeromus", label:"Zeromus"},
    ];
  
    Meteor.forEach(function(value) {
  
      var op = document.createElement("option");
  
      op.value = value.cd;
  
      op.text = value.label;
  
      seller_World.appendChild(op);
  
    });

  }

  function set_seller_Aether() {
  
      seller_World.textContent = null;
  
    var Aether = [  
      {cd:"", label:"ホームを選択して下さい"},
      {cd:"adamantoise", label:"Adamantoise"},
      {cd:"cactuar", label:"Cactuar"},
      {cd:"faerie", label:"Faerie"},
      {cd:"gilgamesh", label:"Gilgamesh"},
      {cd:"jenova", label:"Jenova"},
      {cd:"midgardsormr", label:"Midgardsormr"},
      {cd:"Sargatanas", label:"Sargatanas"},
      {cd:"siren", label:"Siren"},
    ];
  
    Aether.forEach(function(value) {
  
      var op = document.createElement("option");
  
      op.value = value.cd;
  
      op.text = value.label;
  
      seller_World.appendChild(op);
  
    });
  
  }
  function set_seller_Crystal() {
  
      seller_World.textContent = null;
  
    var Crystal = [  
      {cd:"", label:"ホームを選択して下さい"},
      {cd:"balmung", label:"Balmung"},
      {cd:"brynhildr", label:"Brynhildr"},
      {cd:"coeurl", label:"Coeurl"},
      {cd:"diabolos", label:"Diabolos"},
      {cd:"goblin", label:"Goblin"},
      {cd:"malboro", label:"Malboro"},
      {cd:"mateus", label:"Mateus"},
      {cd:"zalera", label:"Zalera"},
    ];
  
    Crystal.forEach(function(value) {
  
      var op = document.createElement("option");
  
      op.value = value.cd;
  
      op.text = value.label;
  
      seller_World.appendChild(op);
  
    });
  }

  function set_seller_Dynamis() {
  
      seller_World.textContent = null;
  
    var Dynamis = [  
      {cd:"", label:"ホームを選択して下さい"},
      {cd:"halicarnassus", label:"halicarnassus"},
      {cd:"maduin", label:"Maduin"},
      {cd:"marilith", label:"Marilith"},
      {cd:"Seraph", label:"Seraph"},
    ];
  
    Dynamis.forEach(function(value) {
  
      var op = document.createElement("option");
  
      op.value = value.cd;
  
      op.text = value.label;
  
      seller_World.appendChild(op);
  
    });
  
  }

  function set_seller_Primal() {
  
      seller_World.textContent = null;
  
    var Primal = [  
      {cd:"", label:"ホームを選択して下さい"},
      {cd:"behemoth", label:"Behemoth"},
      {cd:"excalibur", label:"excalibur"},
      {cd:"exodus", label:"Exodus"},
      {cd:"famfrit", label:"Famfrit"},
      {cd:"hyperion", label:"Hyperion"},
      {cd:"lamia", label:"Lamia"},
      {cd:"leviathan", label:"Leviathan"},
      {cd:"ultros", label:"Ultros"},
    ];
  
    Primal.forEach(function(value) {
  
      var op = document.createElement("option");

      op.value = value.cd;
  
      op.text = value.label;
  
      seller_World.appendChild(op);
  
    });
  }

  function set_seller_Chaos() {
  
      seller_World.textContent = null;
  
    var Chaos = [  
      {cd:"", label:"ホームを選択して下さい"},
      {cd:"cerberus", label:"cerberus"},
      {cd:"louisoix", label:"louisoix"},
      {cd:"moogle", label:"Moogle"},
      {cd:"omega", label:"Omega"},
      {cd:"phantom", label:"Phantom"},
      {cd:"ragnarok", label:"Ragnarok"},
      {cd:"sagittarius", label:"Sagittarius"},
      {cd:"spriggan", label:"Spriggan"},
    ];
  
    Chaos.forEach(function(value) {
  
      var op = document.createElement("option");
      
      op.value = value.cd;
  
      op.text = value.label;
  
      seller_World.appendChild(op);
  
    });
  }

  function set_seller_Light() {
  
      seller_World.textContent = null;
  
    var Light = [  
      {cd:"", label:"ホームを選択して下さい"},
      {cd:"alpha", label:"Alpha"},
      {cd:"lich", label:"Lich"},
      {cd:"odin", label:"Odin"},
      {cd:"phoenix", label:"Phoenix"},
      {cd:"raiden", label:"Raiden"},
      {cd:"shiva", label:"Shiva"},
      {cd:"twintania", label:"Twintania"},
      {cd:"zodiark", label:"Zodiark"},
    ];
  
    Light.forEach(function(value) {
  
      var op = document.createElement("option");
      
      op.value = value.cd;
  
      op.text = value.label;
  
      seller_World.appendChild(op);
  
    });
  }

  function set_seller_Materia() {
  
      seller_World.textContent = null;
  
    var Materia = [ 
      {cd:"", label:"ホームを選択して下さい"},
      {cd:"bismarck", label:"Bismarck"},
      {cd:"ravana", label:"Ravana"},
      {cd:"Sephirot", label:"Sephirot"},
      {cd:"sophia", label:"Sophia"},
      {cd:"zurvan", label:"Zuruvan"}
    ];
  
    Materia.forEach(function(value) {
  
      var op = document.createElement("option");
      
      op.value = value.cd;
  
      op.text = value.label;
  
      seller_World.appendChild(op);
  
    });
  }

  function set_seller_Null() {
  
      seller_World.textContent = null;
  
    var Null = [ 
      {cd:"", label:"ホームを選択して下さい"}
    ];
  
    Null.forEach(function(value) {
  
      var op = document.createElement("option");
      
      op.value = value.cd;
  
      op.text = value.label;
  
      seller_World.appendChild(op);
  
    });
  }



  
