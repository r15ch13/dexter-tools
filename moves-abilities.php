<?php
header("Content-Type: text/html; charset=utf-8");

function objectToArray($o)
{
    $a = array();
    foreach ($o as $k => $v)
    {
        if(is_array($v) || is_object($v))
        {
            $a[$k] = objectToArray($v);
        } else {
            $a[$k] = $v;
        }
    }
    return $a;
}

/*
$moves1 = file_get_contents("move.poke");
$moves1 = json_decode($moves1);
$moves2 = file_get_contents("moves.txt");
$moves2 = json_decode($moves2);
$tmpMoves = array();
$newMoves = array();

foreach ($moves1 as $key1 => $value1) {
    $tmpMoves[$value1->name] = $value1;
}

foreach ($moves2 as $key2 => $value2) {
    if(isset($tmpMoves[$value2->name]))
    {
        $oldMove = $tmpMoves[$value2->name];
        $obj = new stdClass();
        $obj->name = $oldMove->name;
        $obj->name_de = $value2->name_de;
        $obj->name_fr = $value2->name_fr;
        $obj->name_jp = $value2->name_jp;
        $obj->type = $oldMove->type;
        $obj->category = $oldMove->category;
        $obj->power = $oldMove->power;
        $obj->accuracy = $oldMove->accuracy;
        $obj->pp = $oldMove->pp;
        $obj->tm = $oldMove->tm;
        $obj->probability = $oldMove->probability;
        $obj->description = $oldMove->description;
        $newMoves[] = $obj;
    }
    else
    {
        var_dump($value2->name);
    }
}

var_dump(count($tmpMoves));
var_dump(count($newMoves));

$newMoves = json_encode($newMoves, JSON_UNESCAPED_UNICODE);
file_put_contents('new_moves.txt', $newMoves);
//*/


//*
$abilities1 = file_get_contents("ability.poke");
$abilities1 = json_decode($abilities1);
$abilities2 = file_get_contents("abilities.txt");
$abilities2 = json_decode($abilities2);
$tmpAbi = array();
$newAbi = array();

foreach ($abilities1 as $key1 => $value1) {
    $tmpAbi[$value1->name] = $value1;
}

foreach ($abilities2 as $key2 => $value2) {
    if(isset($tmpAbi[$value2->name]))
    {
        $oldAbi = $tmpAbi[$value2->name];
        $obj = new stdClass();
        $obj->name = $oldAbi->name;
        $obj->name_de = $value2->name_de;
        $obj->name_fr = $value2->name_fr;
        $obj->name_jp = $value2->name_jp;
        $obj->description = $oldAbi->description;
        $newAbi[] = $obj;
    }
    else
    {
        var_dump($value2->name);
    }
}

var_dump(count($tmpAbi));
var_dump(count($newAbi));

$newAbi = json_encode($newAbi, JSON_UNESCAPED_UNICODE);
file_put_contents('new_abilities.txt', $newAbi);
//*/