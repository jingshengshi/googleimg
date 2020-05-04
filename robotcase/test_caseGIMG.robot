*** Settings ***
Library    case.TestCmGoogleIMGEN
Library    SeleniumLibrary
Force Tags    gimg
Suite Setup  test0_Setup_EN
Suite Teardown  test0_Teardown_EN

*** Test Case ***
Test google images
    [Tags]    gimg
    test001_find_images_EN


